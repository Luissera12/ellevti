from flask import Flask, jsonify
from flask_cors import CORS

from .config import Config
from .db import create_schema
from .rotas import home_bp, interface_bp, tarefas_bp, stats_bp  # vem do pacote rotas

def create_app(config_overrides: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    if config_overrides:
        app.config.update(config_overrides)

    CORS(app, resources={r"/*": {"origins": "*"}})

    with app.app_context():
        create_schema()

    app.register_blueprint(home_bp)
    app.register_blueprint(interface_bp)
    app.register_blueprint(tarefas_bp)
    app.register_blueprint(stats_bp)

    @app.errorhandler(404)
    def not_found(_e): return jsonify({"erro": "Endpoint não encontrado"}), 404

    @app.errorhandler(500)
    def internal(_e): return jsonify({"erro": "Erro interno do servidor"}), 500

    return app
