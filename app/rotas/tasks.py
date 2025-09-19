from flask import Blueprint, request, jsonify
from ..db import get_conn, row2dict
from ..utils import validar_tarefa, parse_paginacao, STATUS_OK
from ..ia import analisar_tarefa_ia
import logging

# blueprint das rotas de tarefas
bp = Blueprint("tarefas", __name__, url_prefix="/api/tarefas")

@bp.get("")
def listar():
    # pega os filtros da URL
    status_filtro = request.args.get("status")
    prioridade_filtro = request.args.get("prioridade")

    # valida os filtros se foram passados
    if status_filtro and status_filtro not in STATUS_OK:
        return jsonify({"erro": "Status inválido"}), 400
    if prioridade_filtro and prioridade_filtro not in {"baixa", "media", "alta"}:
        return jsonify({"erro": "Prioridade inválida"}), 400

    # paginação - TODO: melhorar isso aqui depois
    page, limit, erro_pag = parse_paginacao()
    if erro_pag: 
        return jsonify({"erro": erro_pag}), 400

    # monta a query dinamicamente com os filtros
    condicoes_where = []
    parametros = []
    
    if status_filtro:
        condicoes_where.append("status = ?")
        parametros.append(status_filtro)
    if prioridade_filtro:
        condicoes_where.append("prioridade = ?")
        parametros.append(prioridade_filtro)
    
    clausula_where = f"WHERE {' AND '.join(condicoes_where)}" if condicoes_where else ""

    # executa as queries
    conn = get_conn()
    try:
        # conta total de registros
        total_registros = conn.execute(f"SELECT COUNT(*) FROM tarefas {clausula_where}", parametros).fetchone()[0]
        
        # calcula offset pra paginação
        offset = (page - 1) * limit
        
        # busca os dados paginados
        query_principal = f"""
            SELECT * FROM tarefas
            {clausula_where}
            ORDER BY data_criacao DESC
            LIMIT ? OFFSET ?
        """
        registros = conn.execute(query_principal, parametros + [limit, offset]).fetchall()
        
        # converte pra dict
        lista_tarefas = [row2dict(linha) for linha in registros]
        total_paginas = (total_registros + limit - 1) // limit
        
        return jsonify({
            "tarefas": lista_tarefas,
            "paginacao": {
                "pagina_atual": page,
                "total_paginas": total_paginas,
                "total_registros": total_registros,
                "registros_por_pagina": limit
            }
        })
    finally:
        conn.close()

@bp.post("")
def criar():
    # pega os dados do request
    dados_request = request.get_json(silent=True) or {}
    
    # valida os dados
    erros_validacao = validar_tarefa(dados_request, precisa_titulo=True)
    if erros_validacao: 
        return jsonify({"erro": "Dados inválidos", "detalhes": erros_validacao}), 422

    # extrai e limpa os dados
    titulo_tarefa = dados_request["titulo"].strip()
    descricao_tarefa = str(dados_request.get("descricao", "")).strip()
    prioridade_tarefa = dados_request.get("prioridade", "media")
    status_tarefa = dados_request.get("status", "pendente")

    # salva no banco
    conn = get_conn()
    try:
        cursor = conn.execute("""
            INSERT INTO tarefas (titulo, descricao, prioridade, status)
            VALUES (?, ?, ?, ?)
        """, (titulo_tarefa, descricao_tarefa, prioridade_tarefa, status_tarefa))
        
        nova_tarefa_id = cursor.lastrowid
        
        # busca a tarefa criada pra retornar
        tarefa_criada = conn.execute("SELECT * FROM tarefas WHERE id = ?", (nova_tarefa_id,)).fetchone()
        conn.commit()
        
        logging.info(f"Nova tarefa criada: ID {nova_tarefa_id}")
        
        return jsonify({
            "mensagem": "Tarefa criada com sucesso", 
            "tarefa": row2dict(tarefa_criada)
        }), 201
        
    except Exception as e:
        logging.error(f"Erro ao criar tarefa: {e}")
        conn.rollback()
        return jsonify({"erro": "Erro interno ao criar tarefa"}), 500
    finally:
        conn.close()

@bp.get("/<int:tarefa_id>")
def buscar(tarefa_id):
    conn = get_conn()
    try:
        r = conn.execute("SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)).fetchone()
        if not r: return jsonify({"erro":"Tarefa não encontrada"}),404
        return jsonify(row2dict(r))
    finally:
        conn.close()

@bp.put("/<int:tarefa_id>")
def atualizar(tarefa_id):
    data = request.get_json(silent=True) or {}
    conn = get_conn()
    try:
        atual = conn.execute("SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)).fetchone()
        if not atual: return jsonify({"erro":"Tarefa não encontrada"}),404
        errs = validar_tarefa(data, True)
        if errs: return jsonify({"erro":"Dados inválidos","detalhes":errs}),422

        titulo = data["titulo"].strip()
        descricao = str(data.get("descricao","")).strip()
        prioridade = data.get("prioridade", atual["prioridade"])
        status = data.get("status",       atual["status"])

        conn.execute("""
          UPDATE tarefas
             SET titulo = ?, descricao = ?, prioridade = ?, status = ?,
                 data_atualizacao = CURRENT_TIMESTAMP
           WHERE id = ?
        """, (titulo,descricao,prioridade,status,tarefa_id))
        r = conn.execute("SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)).fetchone()
        conn.commit()
        return jsonify({"mensagem":"Tarefa atualizada","tarefa":row2dict(r)})
    finally:
        conn.close()

@bp.patch("/<int:tarefa_id>/status")
def alterar_status(tarefa_id: int):
    dados = request.get_json(silent=True) or {}
    novo_status = dados.get("status")
    
    # valida o status
    if novo_status not in STATUS_OK:
        return jsonify({"erro": "Status é obrigatório e deve ser: pendente ou concluida"}), 400

    conn = get_conn()
    try:
        # verifica se a tarefa existe
        tarefa_atual = conn.execute("SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)).fetchone()
        if not tarefa_atual: 
            return jsonify({"erro": "Tarefa não encontrada"}), 404

        # atualiza o status
        conn.execute("""
            UPDATE tarefas
            SET status = ?, data_atualizacao = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (novo_status, tarefa_id))
        
        # busca a tarefa atualizada
        tarefa_atualizada = conn.execute("SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)).fetchone()
        conn.commit()
        
        return jsonify({
            "mensagem": "Status atualizado com sucesso",
            "tarefa": row2dict(tarefa_atualizada)
        })
        
    except Exception as e:
        logging.error(f"Erro ao alterar status da tarefa {tarefa_id}: {e}")
        return jsonify({"erro": "Erro interno"}), 500
    finally:
        conn.close()

@bp.delete("/<int:tarefa_id>")
def deletar(tarefa_id: int):
    conn = get_conn()
    try:
        r = conn.execute("SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)).fetchone()
        if not r: return jsonify({"erro":"Tarefa não encontrada"}),404
        conn.execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))
        conn.commit()
        return jsonify({"mensagem":"Tarefa deletada","tarefa":row2dict(r)})
    finally:
        conn.close()

@bp.post("/<int:tarefa_id>/analisar")
def analisar(tarefa_id: int):
    conn = get_conn()
    try:
        t = conn.execute("SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)).fetchone()
    finally:
        conn.close()
    if not t: return jsonify({"erro":"Tarefa não encontrada"}),404

    tarefa = {"id":t["id"],"titulo":t["titulo"],"descricao":t["descricao"],"prioridade":t["prioridade"]}
    try:
        analise = analisar_tarefa_ia(tarefa)
        status_code = 200
        if analise.get("justificativa","").startswith("Falha ao chamar IA"):
            status_code = 200  # ainda devolve algo útil
    except RuntimeError:
        return jsonify({
            "tarefa": tarefa,
            "analise": {"tempo_estimado":4,"complexidade":"medio","justificativa":"IA off (defina OPENAI_API_KEY)."}
        }), 503

    return jsonify({"tarefa": tarefa, "analise": analise}), status_code
