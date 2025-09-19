
import logging
import os
from dotenv import load_dotenv

# carrega as variáveis do arquivo .env
load_dotenv()

from app import create_app  
from app.db import get_conn

# cria a aplicação
app = create_app()

if __name__ == "__main__":
    # popula o banco com dados de exemplo se estiver vazio
    with app.app_context():
        conexao = get_conn()
        try:
            quantidade_tarefas = conexao.execute("SELECT COUNT(*) FROM tarefas").fetchone()[0]
            print(f"Tarefas no banco: {quantidade_tarefas}")  # debug esquecido
            
            if quantidade_tarefas == 0:
                print("Banco vazio, inserindo dados de exemplo...")
                tarefas_exemplo = [
                    ("Implementar login com JWT", "Sistema de autenticação completo", "alta", "pendente"),
                    ("Criar testes unitários", "Cobertura dos endpoints principais", "media", "pendente"),
                    ("Documentar API", "README e comentários no código", "baixa", "concluida"),
                    ("Otimizar consultas SQL", "Melhorar performance do banco", "media", "pendente"),
                    ("Deploy em produção", "Configurar servidor e CI/CD", "alta", "concluida"),
                ]
                
                for tarefa in tarefas_exemplo:
                    conexao.execute(
                        "INSERT INTO tarefas (titulo, descricao, prioridade, status) VALUES (?, ?, ?, ?)", 
                        tarefa
                    )
                conexao.commit()
                print("✅ Dados de exemplo inseridos com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao inserir dados: {e}")
        finally:
            conexao.close()

    # configurações do servidor
    porta = app.config["PORT"]
    modo_debug = app.config["DEBUG"]
    
    print(f"🚀 Iniciando servidor...")
    print(f"📍 API: http://localhost:{porta}")
    print(f"🖥️  Interface: http://localhost:{porta}/interface")
    print(f"🔧 Debug mode: {modo_debug}")
    
    app.run(host="0.0.0.0", port=porta, debug=modo_debug)
