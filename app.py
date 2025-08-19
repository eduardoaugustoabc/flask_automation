from flask import Flask, request, jsonify
from medicalsys.client import MedicalSysError
from medicalsys.agenda_service import *
from medicalsys.client import MedicalSysClient

app = Flask(__name__)

# opcional: rota ping
@app.get("/health")
def health():
    return {"status": "ok"}, 200

# GET /agenda  -> proxy para GET {BASE}/agenda/
@app.get("/agenda")
def http_get_agenda():
    try:
        # todos os filtros que você passar na querystring são repassados
        filtros = dict(request.args)
        data = listar_agenda(filtros)
        return jsonify(data), 200
    except MedicalSysError as e:
        return jsonify({"error": str(e)}), 502
    except Exception as e:
        return jsonify({"error": f"Falha inesperada: {e}"}), 500

# GET /agenda/<id>  -> (opcional) consultar um agendamento específico
@app.get("/agenda/<agendamento_id>")
def http_get_agendamento_id(agendamento_id):
    try:
        client = MedicalSysClient()
        data = client.get_agendamento(agendamento_id)
        return jsonify(data), 200
    except MedicalSysError as e:
        return jsonify({"error": str(e)}), 502
    except Exception as e:
        return jsonify({"error": f"Falha inesperada: {e}"}), 500

# POST /agenda  -> proxy para POST {BASE}/agenda/
@app.post("/agenda")
def http_post_agenda():
    try:
        payload = request.get_json(silent=True) or {}
        if not payload:
            return jsonify({"error": "Corpo JSON obrigatório."}), 400
        data = criar_agendamento(payload)
        # a API costuma retornar 201 ao criar; se não retornar corpo, devolvemos {}
        return jsonify(data), 201
    except MedicalSysError as e:
        return jsonify({"error": str(e)}), 502
    except Exception as e:
        return jsonify({"error": f"Falha inesperada: {e}"}), 500

@app.put("/agenda/<agendamento_id>")
def http_put_agenda(agendamento_id):
    try:
        payload = request.get_json(silent=True) or {}
        if not payload:
            return jsonify({"error": "Corpo JSON obrigatório."}), 400
        data = atualizar_agendamento(agendamento_id, payload)
        return jsonify(data), 200
    except MedicalSysError as e:
        return jsonify({"error": str(e)}), 502
    except Exception as e:
        return jsonify({"error": f"Falha inesperada: {e}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)