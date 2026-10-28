import http.server
import json
import os
import sys

PORT = 8080

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        env_existe = os.path.exists(".env")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        respuesta = {
            "estado": "inseguro" if env_existe else "limpio",
            "archivo_env_filtrado_en_imagen": env_existe,
            "alerta": "🚨 PELIGRO: El archivo .env con contraseñas está dentro de la imagen!" if env_existe else "✅ LIMPIO: La imagen no contiene secretos ni archivos locales indebidos."
        }
        self.wfile.write(json.dumps(respuesta, indent=2, ensure_ascii=False).encode("utf-8"))

    def log_message(self, formato, *args):
        sys.stdout.write(f"[{self.log_date_time_string()}] {formato % args}\n")
        sys.stdout.flush()

if __name__ == "__main__":
    servidor = http.server.HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"🚀 Servidor corriendo en puerto {PORT}...")
    servidor.serve_forever()
