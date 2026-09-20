from flask import Flask, request, jsonify
import os
import socket
import psycopg2

app = Flask(__name__)

DB_PARAMS = {
    "host": os.getenv("DB_HOST", "pagosya-db"),
    "dbname": os.getenv("DB_NAME", "pagosya"),
    "user": os.getenv("DB_USER", "pagosya"),
    "password": os.getenv("DB_PASS", "pagosya123"),
}


def get_db():
    return psycopg2.connect(**DB_PARAMS)


@app.after_request
def permitir_origen(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.route("/health")
def health():
    return jsonify(status="ok", servidor=socket.gethostname(),
                   ip=request.host)


@app.route("/pagos", methods=["POST"])
def crear_pago():
    datos = request.get_json(force=True)
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO pagos (monto, cliente) VALUES (%s, %s) RETURNING id",
        (datos["monto"], datos.get("cliente", "anonimo")),
    )
    pid = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(estado="registrado", id_pago=pid, monto=datos["monto"]), 201


@app.route("/pagos", methods=["GET"])
def listar_pagos():
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)