from flask import Blueprint, jsonify
from ..db import get_conn

bp = Blueprint("stats", __name__, url_prefix="/api")

@bp.get("/estatisticas")
def estatisticas():
    conn = get_conn()
    try:
        total     = conn.execute("SELECT COUNT(*) FROM tarefas").fetchone()[0]
        pendentes = conn.execute("SELECT COUNT(*) FROM tarefas WHERE status='pendente'").fetchone()[0]
        concluidas= conn.execute("SELECT COUNT(*) FROM tarefas WHERE status='concluida'").fetchone()[0]
        prios     = conn.execute("SELECT prioridade, COUNT(*) c FROM tarefas GROUP BY prioridade").fetchall()
        por_prio  = {r["prioridade"]: r["c"] for r in prios}
        return jsonify({"total": total, "pendentes": pendentes, "concluidas": concluidas, "por_prioridade": por_prio})
    finally:
        conn.close()
