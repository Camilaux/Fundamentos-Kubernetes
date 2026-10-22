"""
Servidor HTTP minimalista en Python sin dependencias externas.
Ideal para entender cómo empaquetar una aplicación con variables de entorno
y probarla primero en Docker y luego en Kubernetes.
"""
import http.server
import json
import os
import socket
import sys

PORT = int(os.environ.get("PORT", 8080))
MENSAJE = os.environ.get("MENSAJE", "¡Hola desde mi contenedor en Cloud Native Medellín! 🏔️☕")


class SimpleHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Endpoint de salud (Health check para Kubernetes)
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "saludable": True}).encode("utf-8"))
            return

        # Endpoint principal
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()

        # Inspección del usuario que ejecuta el proceso (Buenas prácticas de seguridad)
        usuario = "desconocido"
        uid = -1
        try:
            import pwd
            uid = os.getuid()
            usuario = pwd.getpwuid(uid).pw_name
        except Exception:
            usuario = os.environ.get("USER", "appuser")

        respuesta = {
            "mensaje": MENSAJE,
            "hostname_o_pod": socket.gethostname(),
            "puerto": PORT,
            "usuario_proceso": f"{usuario} (UID: {uid})",
            "es_root": (uid == 0),
            "orquestador": "Listo para correr en Kubernetes",
            "comunidad": "Cloud Native Medellín 🏔️☕"
        }
        self.wfile.write(json.dumps(respuesta, indent=2, ensure_ascii=False).encode("utf-8"))

    def log_message(self, formato, *args):
        # Imprime logs legibles en la salida estándar (para docker logs o kubectl logs)
        sys.stdout.write(f"[{self.log_date_time_string()}] {formato % args}\n")
        sys.stdout.flush()


if __name__ == "__main__":
    servidor = http.server.HTTPServer(("0.0.0.0", PORT), SimpleHandler)
    try:
        import pwd
        u_actual = pwd.getpwuid(os.getuid()).pw_name
        uid_actual = os.getuid()
    except Exception:
        u_actual, uid_actual = "appuser", 10001
    print(f"🚀 Servidor escuchando en http://0.0.0.0:{PORT} como '{u_actual}' (UID: {uid_actual})...")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido limpiamente.")
        servidor.server_close()

