API de Gerenciamento de Tarefas

Sistema para gerenciar tarefas com análise por IA usando Flask.

Tecnologias:
Python 3.8+, Flask, SQLite, OpenAI GPT-3.5-turbo, Flask-CORS, python-dotenv

Funcionalidades:
CRUD completo de tarefas
Filtros por status e prioridade  
Paginação na listagem
Análise de tarefas com IA
Estatísticas básicas

Instalação:

1. Clonar o repositório
2. Criar ambiente virtual: python -m venv venv
3. Ativar ambiente: venv\Scripts\activate (Windows) ou source venv/bin/activate (Linux/Mac)
4. Instalar dependências: pip install -r requirements.txt
5. Criar arquivo .env com: OPENAI_API_KEY=()
6. Executar: python run.py

Endpoints:
GET /api/tarefas - Lista tarefas
POST /api/tarefas - Cria tarefa
GET /api/tarefas/{id} - Busca tarefa
PUT /api/tarefas/{id} - Atualiza tarefa
DELETE /api/tarefas/{id} - Remove tarefa
POST /api/tarefas/{id}/analisar - Análise IA
GET /api/estatisticas - Estatísticas

Interface de teste: http://localhost:5000/interface
