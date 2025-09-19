import os
from flask import Blueprint, jsonify, send_from_directory

bp = Blueprint("interface", __name__)

@bp.route("/interface")
def interface():
    base = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    html = os.path.join(base, "interface.html")
    if os.path.exists(html): 
        return send_from_directory(base, "interface.html")
    return jsonify({"erro":"Arquivo interface.html não encontrado"}), 404
