# Funções auxiliares - validação etc
from typing import Any, Dict, List, Optional, Tuple
from flask import request

# TODO: talvez criar um enum aqui depois
PRIORIDADES_OK = {"baixa","media","alta"}
STATUS_OK = {"pendente","concluida"}

def validar_tarefa(dados, precisa_titulo=True):
    # valida se os dados da tarefa tão certos
    erros = []
    if not dados:
        return ["Dados vazios ou inválidos"]
    
    # titulo obrigatório na criação
    if precisa_titulo and not dados.get("titulo", "").strip():
        erros.append("Título é obrigatório")
    
    # checa prioridade
    if "prioridade" in dados and dados["prioridade"] not in PRIORIDADES_OK:
        erros.append("Prioridade deve ser: baixa, media ou alta")
    
    # checa status  
    if "status" in dados and dados["status"] not in STATUS_OK:
        erros.append("Status deve ser: pendente ou concluida")
    
    return erros

def parse_paginacao():
    # pega os parametros de paginação da url
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
    except ValueError:
        # se não conseguir converter, usa padrão
        return 1, 10, "page/limit tem que ser números"
    
    # validações básicas
    if page < 1: 
        page = 1
    if limit < 1: 
        limit = 10
    if limit > 100:  # evita queries muito pesadas
        limit = 100
        
    return page, limit, None
