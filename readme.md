API de Gerenciamento de Tarefas com IA

API REST desenvolvida em Python/Flask para gerenciamento de tarefas com funcionalidade de análise usando inteligência artificial.

Tecnologias Utilizadas

Backend: Python 3.8+ com Flask
Banco de dados: SQLite 
IA: OpenAI GPT-3.5-turbo
Outras dependências: Flask-CORS, python-dotenv

Funcionalidades

<<<<<<< HEAD
CRUD completo de tarefas (criar, listar, buscar, atualizar, excluir)
Filtros por status (pendente/concluída) e prioridade (baixa/média/alta)
Paginação na listagem de tarefas
Análise automática de tarefas com IA (tempo estimado, complexidade, justificativa)
Estatísticas básicas do sistema
Interface web para testes

Instalação e Execução

1. Clone o repositório:
git clone https://github.com/Luissera12/ellevti.git
cd ellevti

2. Crie e ative o ambiente virtual:
python -m venv venv
venv\Scripts\activate (Windows)
source venv/bin/activate (Linux/Mac)

3. Instale as dependências:
pip install -r requirements.txt

4. Configure a API da OpenAI:
Crie um arquivo .env na raiz do projeto com:
OPENAI_API_KEY=sua_chave_da_openai_aqui
PORT=5000
DEBUG=true

Para obter uma chave da OpenAI:
- Acesse https://platform.openai.com/
- Crie uma conta ou faça login
- Vá em API Keys e gere uma nova chave
- Cole a chave no arquivo .env

5. Execute a aplicação:
python run.py

A API estará disponível em http://localhost:5000
Interface de teste em http://localhost:5000/interface

Documentação da API

Base URL: http://localhost:5000

Estrutura da Tarefa:
{
  "id": 1,
  "titulo": "Implementar autenticação",
  "descricao": "Sistema de login com JWT",
  "prioridade": "alta",
  "status": "pendente", 
  "data_criacao": "2024-01-01T10:00:00",
  "data_atualizacao": "2024-01-01T10:00:00"
}
=======
1. Clonar o repositório
2. Criar ambiente virtual: python -m venv venv
3. Ativar ambiente: venv\Scripts\activate (Windows) ou source venv/bin/activate (Linux/Mac)
4. Instalar dependências: pip install -r requirements.txt
5. Criar arquivo .env com: OPENAI_API_KEY=()
6. Executar: python run.py
>>>>>>> b0f2ea50a8d8a6f74c2def366b246f5b77f77e9a

Endpoints:

<<<<<<< HEAD
GET /api/tarefas
Lista todas as tarefas com paginação e filtros
Parâmetros opcionais:
- status: pendente ou concluida
- prioridade: baixa, media ou alta  
- page: número da página (padrão: 1)
- limit: registros por página (padrão: 10, máximo: 100)

POST /api/tarefas
Cria uma nova tarefa
Body (JSON):
{
  "titulo": "string (obrigatório)",
  "descricao": "string (opcional)",
  "prioridade": "baixa|media|alta (opcional, padrão: media)",
  "status": "pendente|concluida (opcional, padrão: pendente)"
}

GET /api/tarefas/{id}
Busca uma tarefa específica por ID

PUT /api/tarefas/{id}  
Atualiza uma tarefa existente
Body: mesma estrutura do POST

PATCH /api/tarefas/{id}/status
Altera apenas o status de uma tarefa
Body: {"status": "pendente|concluida"}

DELETE /api/tarefas/{id}
Remove uma tarefa

POST /api/tarefas/{id}/analisar
Analisa uma tarefa com IA
Retorna: tempo estimado (horas), complexidade e justificativa

GET /api/estatisticas
Retorna estatísticas gerais do sistema

Exemplos de Uso

Criar uma tarefa:
curl -X POST http://localhost:5000/api/tarefas \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Implementar login", "descricao": "Sistema de autenticação", "prioridade": "alta"}'

Listar tarefas pendentes:
curl "http://localhost:5000/api/tarefas?status=pendente&page=1&limit=5"

Analisar tarefa com IA:
curl -X POST http://localhost:5000/api/tarefas/1/analisar

Alterar status para concluída:
curl -X PATCH http://localhost:5000/api/tarefas/1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "concluida"}'

Estrutura do Projeto

app/
├── __init__.py          # Configuração da aplicação Flask
├── config.py            # Configurações e variáveis de ambiente  
├── db.py               # Schema do banco e conexões
├── ia.py               # Integração com OpenAI
├── utils.py            # Validações e utilitários
└── rotas/              # Blueprints das rotas
    ├── home.py         # Rota principal
    ├── tasks.py        # CRUD de tarefas
    ├── stats.py        # Estatísticas
    └── interface.py    # Interface web
run.py                  # Ponto de entrada da aplicação
interface.html          # Interface web para testes
requirements.txt        # Dependências Python
=======
Interface de teste: http://localhost:5000/interface
>>>>>>> b0f2ea50a8d8a6f74c2def366b246f5b77f77e9a
