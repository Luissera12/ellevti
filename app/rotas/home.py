from flask import Blueprint, jsonify

bp = Blueprint("home", __name__)

@bp.route("/")
def home():
    return jsonify({
        "mensagem":"API Tarefas + IA",
        "versao":"1.1.0",
        "interface":"http://localhost:5000/interface",
        "endpoints":{
            "GET /interface":"HTML de teste",
            "GET /api/tarefas":"Listar",
            "GET /api/tarefas/<id>":"Buscar",
            "POST /api/tarefas":"Criar",
            "PUT /api/tarefas/<id>":"Atualizar",
            "PATCH /api/tarefas/<id>/status":"Status",
            "DELETE /api/tarefas/<id>":"Excluir",
            "POST /api/tarefas/<id>/analisar":"Estimativa (ia)",
            "GET /api/estatisticas":"Resumo",
        }
    })
