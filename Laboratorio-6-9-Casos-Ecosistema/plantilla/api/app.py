from flask import Flask, request, jsonify
import os
import socket

app = Flask(__name__)

# Modo "memoria" (Caso 2, sin DB) vs modo "postgres" (Caso 3, DB_HOST definido)
USE_DB = os.getenv("DB_HOST") is not None
MEMORIA = []

DB_PARAMS = {
    "host": os.getenv("DB_HOST", "datosya-db"),
    "dbname": os.getenv("DB_NAME", "pagosya"),
    "user": os.getenv("DB_USER", "pagosya"),
    "password": os.getenv("DB_PASS", "pagosya123"),
}


def get_db():
    import psycopg2
    return psycopg2.connect(**DB_PARAMS)


@app.after_request
def permitir_origen(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route("/health")
def health():
    return jsonify(status="ok", servidor=socket.gethostname(),
                   ip=request.host,
                   almacenado="postgres" if USE_DB else "memoria")


@app.route("/pagos", methods=["POST"])
def crear_pago():
    datos = request.get_json(force=True)
    monto = datos["monto"]
    cliente = datos.get("cliente", "anonimo")
    if USE_DB:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO pagos (monto, cliente) VALUES (%s, %s) RETURNING id",
            (monto, cliente),
        )
        pid = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
    else:
        pid = len(MEMORIA) + 1
        MEMORIA.append({"id": pid, "cliente": cliente, "monto": monto})
    return jsonify(estado="registrado", id_pago=pid, monto=monto,
                   almacenado="postgres" if USE_DB else "memoria"), 201


@app.route("/pagos", methods=["GET"])
def listar_pagos():
    if USE_DB:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, cliente, monto, creado_en FROM pagos ORDER BY id DESC")
        filas = [
            {
                "id": r[0],
                "cliente": r[1],
                "monto": float(r[2]),
                "creado_en": r[3].isoformat(),
            }
            for r in cur.fetchall()
        ]
        cur.close()
        conn.close()
        return jsonify(pagos=filas)
    return jsonify(pagos=[{
        "id": p["id"],
        "cliente": p["cliente"],
        "monto": float(p["monto"]),
        "creado_en": "memoria",
    } for p in MEMORIA])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)