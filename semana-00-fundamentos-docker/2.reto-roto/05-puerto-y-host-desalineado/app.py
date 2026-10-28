import http.server
import json
import os
import sys

# ❌ ERROR 1: La aplicación está escuchando en el puerto 5000,
# pero el Dockerfile expone el 8080 y docker run mapea el 8080.
PORT = int(os.environ.get("PORT", 5000))

# ❌ ERROR 2: Escucha únicamente en la interfaz local interna '127.0.0.1' del contenedor.
# En Docker, para que el tráfico externo que llega por el mapeo de puertos (-p)
# pueda entrar al proceso, se DEBE escuchar en todas las interfaces ('0.0.0.0').
HOST = "127.0.0.1"


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        respuesta = {
            "estado": "conectado",
            "mensaje": "🎉 ¡Felicidades! Lograste alinear el Host y el Puerto en Docker.",
            "host": HOST,
            "puerto": PORT
        }
        self.wfile.write(json.dumps(respuesta, indent=2, ensure_ascii=False).encode("utf-8"))

    def log_message(self, formato, *args):
        sys.stdout.write(f"[{self.log_date_time_string()}] {formato % args}\n")
        sys.stdout.flush()


if __name__ == "__main__":
    print(f"🚀 Iniciando servidor en http://{HOST}:{PORT}...")
    servidor = http.server.HTTPServer((HOST, PORT), Handler)
    servidor.serve_forever()
