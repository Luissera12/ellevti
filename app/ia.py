# Integração com a API da OpenAI pra analisar as tarefas
import json
import logging
from typing import Dict, Any
from flask import current_app

def analisar_tarefa_ia(tarefa: Dict[str, Any]) -> Dict[str, Any]:
    # verifica se tem a chave da API configurada
    api_key = current_app.config.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("IA_OFF")

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
    except Exception as e:
        logging.error(f"Erro ao inicializar OpenAI: {e}")
        raise RuntimeError("IA_INIT_FAIL")

    # monta o prompt pra IA
    prompt_texto = f"""
Você é um tech lead experiente. Analise a tarefa abaixo e retorne APENAS um JSON válido:

{{
  "tempo_estimado": <número entre 1 e 40>,
  "complexidade": "simples" | "medio" | "complexo", 
  "justificativa": "<explicação com até 240 caracteres>"
}}

Dados da tarefa:
- Título: {tarefa['titulo']}
- Descrição: {tarefa.get('descricao') or 'Sem descrição detalhada'}
- Prioridade: {tarefa['prioridade']}
"""

    try:
        # faz a chamada pra API
        resposta = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um especialista em estimativas de desenvolvimento. Retorne apenas JSON válido."},
                {"role": "user", "content": prompt_texto}
            ],
            max_tokens=150, 
            temperature=0.3  # um pouco de variação nas respostas
        )
        
        # pega o conteúdo da resposta
        conteudo_resposta = (resposta.choices[0].message.content or "").strip()
        
        # tenta fazer parse do JSON
        try:
            dados_analise = json.loads(conteudo_resposta)
        except json.JSONDecodeError:
            # se não conseguir fazer parse, retorna dados padrão
            logging.warning("IA retornou JSON inválido")
            dados_analise = {}
        
        # valida e limpa os dados
        tempo_est = dados_analise.get("tempo_estimado")
        if not isinstance(tempo_est, int): 
            tempo_est = 4  # padrão
        tempo_est = max(1, min(40, tempo_est))  # entre 1 e 40 horas
        
        complexidade = dados_analise.get("complexidade")
        if complexidade not in ["simples", "medio", "complexo"]: 
            complexidade = "medio"
        
        justificativa = dados_analise.get("justificativa") or "Análise baseada em experiência de desenvolvimento."
        if len(justificativa) > 240: 
            justificativa = justificativa[:237] + "..."  # trunca se muito grande
            
        return {
            "tempo_estimado": tempo_est,
            "complexidade": complexidade, 
            "justificativa": justificativa
        }
        
    except Exception as erro:
        logging.error(f"Erro ao chamar OpenAI: {erro}")
        # retorna algo útil mesmo com erro
        return {
            "tempo_estimado": 4,
            "complexidade": "medio", 
            "justificativa": "Erro na análise automática - estimativa padrão aplicada."
        }
