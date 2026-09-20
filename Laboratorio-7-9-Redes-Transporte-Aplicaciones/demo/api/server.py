from flask import Flask, request
import socket

app = Flask(__name__)


@app.route('/')
def home():
    return {
        "mensaje": "El mensaje llegó al destino",
        "servidor": socket.gethostbyname(socket.gethostname()),
        "nombre": "api-servicio",
        "protocolo": "TCP",
        "puerto": 5000,
        "cliente": request.remote_addr,
        "consulta": {
            "metodo": request.method,
            "path": request.path,
            "user_agent": request.headers.get('User-Agent'),
        }
    }


@app.route('/health')
def health():
    return {"status": "ok"}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)