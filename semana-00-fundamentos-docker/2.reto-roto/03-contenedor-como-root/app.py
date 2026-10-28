import http.server
import json
import os
import sys

PORT = 8080

class SimpleHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        uid = os.getuid() if hasattr(os, "getuid") else -1
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        respuesta = {
            "estado": "alerta" if uid == 0 else "seguro",
            "uid_actual": uid,
            "es_root": (uid == 0),
            "mensaje": "⚠️ ALERTA: Este contenedor está corriendo como superusuario (root)!" if uid == 0 else "✅ EXCELENTE: El contenedor corre con un usuario sin privilegios."
        }
        self.wfile.write(json.dumps(respuesta, indent=2, ensure_ascii=False).encode("utf-8"))

    def log_message(self, formato, *args):
        sys.stdout.write(f"[{self.log_date_time_string()}] {formato % args}\n")
        sys.stdout.flush()

if __name__ == "__main__":
    servidor = http.server.HTTPServer(("0.0.0.0", PORT), SimpleHandler)
    uid = os.getuid() if hasattr(os, "getuid") else -1
    print(f"🚀 Iniciando servidor en puerto {PORT} con UID: {uid}...")
    servidor.serve_forever()
