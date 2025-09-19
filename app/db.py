import sqlite3
from flask import current_app

# esquema do banco - estrutura das tabelas
SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

-- tabela principal de tarefas
CREATE TABLE IF NOT EXISTS tarefas (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  titulo TEXT NOT NULL,
  descricao TEXT,
  prioridade TEXT DEFAULT 'media' CHECK(prioridade IN ('baixa','media','alta')),
  status TEXT DEFAULT 'pendente' CHECK(status IN ('pendente','concluida')),
  data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- indices pra melhorar performance
CREATE INDEX IF NOT EXISTS idx_tarefas_status      ON tarefas(status);
CREATE INDEX IF NOT EXISTS idx_tarefas_prioridade  ON tarefas(prioridade);
CREATE INDEX IF NOT EXISTS idx_tarefas_data        ON tarefas(data_criacao);
"""

def get_conn():
    # conecta no banco sqlite
    conexao = sqlite3.connect(current_app.config["DATABASE"])
    conexao.row_factory = sqlite3.Row  # pra retornar como dict
    return conexao

def create_schema():
    # cria as tabelas se não existirem
    conexao = get_conn()
    try:
        conexao.executescript(SCHEMA_SQL)
        conexao.commit()
        print("📄 Schema do banco criado/verificado")  # debug esquecido
    finally:
        conexao.close()

def row2dict(linha_banco):
    # converte row do sqlite pra dict python
    return dict(linha_banco)
