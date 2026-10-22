import http.server
import json
import os
import sys

# ❌ La aplicación requiere obligatoriamente una variable de entorno para inicializarse
TOKEN = os.environ.get("APP_SECRET_TOKEN")
PORT = int(os.environ.get("PORT", 8080))

if not TOKEN:
    print("💥 ERROR FATAL: La variable de entorno obligatoria 'APP_SECRET_TOKEN' no fue proporcionada.", file=sys.stderr)
    print("Pista: Puedes definirla en el Dockerfile con 'ENV' o al correr el contenedor con 'docker run -e APP_SECRET_TOKEN=...'", file=sys.stderr)
    sys.exit(1)


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        respuesta = {
            "estado": "activo",
            "mensaje": "🎉 ¡Excelente! La variable de entorno fue configurada correctamente.",
            "token_configurado": TOKEN,
            "puerto": PORT
        }
        self.wfile.write(json.dumps(respuesta, indent=2, ensure_ascii=False).encode("utf-8"))

    def log_message(self, formato, *args):
        sys.stdout.write(f"[{self.log_date_time_string()}] {formato % args}\n")
        sys.stdout.flush()


if __name__ == "__main__":
    print(f"🚀 Servidor iniciado con éxito con token '{TOKEN}' en puerto {PORT}...")
    servidor = http.server.HTTPServer(("0.0.0.0", PORT), Handler)
    servidor.serve_forever()
