"""
Microservicio Backend: Greca Central de Tintos.
Provee endpoints de inventario y preparación de café para otros contenedores.
Escucha en puerto 8080 (sin privilegios).
"""
import http.server
import json
import os
import socket
import sys
import time

PORT = int(os.environ.get("PORT", 8080))
NOMBRE_SERVICIO = os.environ.get("NOMBRE_SERVICIO", "greca-central")
INVENTARIO_TINTOS = 100

class GrecaHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global INVENTARIO_TINTOS

        # Health check
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "servicio": NOMBRE_SERVICIO}).encode("utf-8"))
            return

        # Despacho de tinto a otros carritos en la red
        if self.path == "/despachar-tinto":
            INVENTARIO_TINTOS -= 1
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            respuesta = {
                "origen": NOMBRE_SERVICIO,
                "hostname_contenedor": socket.gethostname(),
                "ip_privada": socket.gethostbyname(socket.gethostname()),
                "mensaje": "☕ ¡Tinto despachado desde la Greca Central!",
                "tintos_restantes_inventario": INVENTARIO_TINTOS,
                "red_docker": "Conexión exitosa mediante DNS interno de Docker"
            }
            self.wfile.write(json.dumps(respuesta, indent=2, ensure_ascii=False).encode("utf-8"))
            return

        # Info del servicio
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        info = {
            "servicio": NOMBRE_SERVICIO,
            "descripcion": "Backend central de café en la red interna",
            "hostname": socket.gethostname(),
            "ip_interna": socket.gethostbyname(socket.gethostname()),
            "puerto": PORT,
            "endpoints_disponibles": ["/despachar-tinto", "/health"]
        }
        self.wfile.write(json.dumps(info, indent=2, ensure_ascii=False).encode("utf-8"))

    def log_message(self, formato, *args):
        sys.stdout.write(f"[{self.log_date_time_string()}] {formato % args}\n")
        sys.stdout.flush()

if __name__ == "__main__":
    server = http.server.HTTPServer(("0.0.0.0", PORT), GrecaHandler)
    mi_ip = socket.gethostbyname(socket.gethostname())
    print(f"☕ Backend [{NOMBRE_SERVICIO}] escuchando en http://0.0.0.0:{PORT} (IP interna: {mi_ip})...")
    server.serve_forever()
