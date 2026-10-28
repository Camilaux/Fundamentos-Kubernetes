"""
Microservicio: Libro Contable de Ventas de Tinto.
Demuestra la persistencia de datos en Docker usando volúmenes.
Escribe y lee registros en el archivo '/app/datos/ventas.json'.
"""
import datetime
import http.server
import json
import os
import socket
import sys
import urllib.parse

PORT = int(os.environ.get("PORT", 8080))
DATA_DIR = os.environ.get("DATA_DIR", "/app/datos")
DATA_FILE = os.path.join(DATA_DIR, "ventas.json")

# Asegurar que el directorio de datos existe
os.makedirs(DATA_DIR, exist_ok=True)

def cargar_ventas():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def guardar_venta(tipo_cafe, cliente):
    ventas = cargar_ventas()
    nueva_venta = {
        "id": len(ventas) + 1,
        "producto": tipo_cafe,
        "cliente": cliente,
        "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "hostname_contenedor": socket.gethostname()
    }
    ventas.append(nueva_venta)
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(ventas, f, indent=2, ensure_ascii=False)
    except PermissionError as e:
        sys.stderr.write(f"🛑 Error de permisos al escribir en {DATA_FILE}: {e}\n")
        sys.stderr.write("💡 Pista: Si usas Bind Mount, la carpeta del host debe tener permisos de escritura (ej: chmod 777 mis-datos-locales).\n")
        sys.stderr.flush()
        raise
    return nueva_venta

HTML_PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>💾 Almacenamiento y Volúmenes en Docker — Cloud Native Medellín</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0a0e17;
      --card-bg: rgba(18, 24, 38, 0.9);
      --border: rgba(245, 158, 11, 0.25);
      --gold: #f59e0b;
      --green: #10b981;
      --cyan: #06b6d4;
      --red: #ef4444;
      --text: #f9fafb;
      --muted: #9ca3af;
      --code-bg: #030712;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Outfit', sans-serif;
      background: radial-gradient(circle at 50% 10%, rgba(245, 158, 11, 0.15), transparent 45%), var(--bg);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 2rem 1rem;
    }
    .container {
      max-width: 820px;
      width: 100%;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 24px;
      padding: 2.5rem;
      box-shadow: 0 25px 60px rgba(0,0,0,0.7);
    }
    .badge {
      display: inline-block;
      background: rgba(245, 158, 11, 0.15);
      color: var(--gold);
      border: 1px solid var(--gold);
      padding: 0.35rem 0.85rem;
      border-radius: 9999px;
      font-size: 0.82rem;
      font-weight: 600;
      margin-bottom: 1.2rem;
    }
    h1 { font-size: 2.2rem; margin-bottom: 0.4rem; }
    p.lead { color: var(--muted); margin-bottom: 1.5rem; }
    .status-panel {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 1rem;
      margin-bottom: 1.8rem;
    }
    .status-card {
      background: rgba(0,0,0,0.3);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 14px;
      padding: 1rem 1.2rem;
    }
    .status-title { font-size: 0.75rem; text-transform: uppercase; color: var(--muted); margin-bottom: 0.3rem; }
    .status-value { font-family: 'JetBrains Mono', monospace; font-size: 1.1rem; font-weight: 700; color: #fff; }
    .action-bar {
      display: flex;
      flex-wrap: wrap;
      gap: 0.8rem;
      margin-bottom: 1.8rem;
    }
    .btn {
      appearance: none;
      border: none;
      cursor: pointer;
      font-family: inherit;
      font-size: 0.92rem;
      font-weight: 600;
      padding: 0.75rem 1.4rem;
      border-radius: 12px;
      transition: transform 0.2s;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
    }
    .btn-gold { background: linear-gradient(135deg, var(--gold), #d97706); color: #0b0f19; }
    .btn-cyan { background: rgba(6, 182, 212, 0.15); color: var(--cyan); border: 1px solid var(--cyan); }
    .btn:hover { transform: translateY(-2px); }
    .table-box {
      background: var(--code-bg);
      border: 1px solid rgba(255,255,255,0.1);
      border-radius: 14px;
      overflow-x: auto;
      max-height: 280px;
      padding: 1rem;
    }
    table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
    th { text-align: left; padding: 0.6rem; color: var(--gold); border-bottom: 1px solid rgba(255,255,255,0.1); }
    td { padding: 0.6rem; border-bottom: 1px solid rgba(255,255,255,0.05); }
    .empty-msg { text-align: center; color: var(--muted); padding: 1.5rem; font-style: italic; }
  </style>
</head>
<body>
  <div class="container">
    <span class="badge">💾 Almacenamiento & Volúmenes en Docker</span>
    <h1>Libro Contable de Tintos</h1>
    <p class="lead">Demostración de persistencia: ¿Qué pasa con los datos cuando el contenedor se destruye con <code>docker rm -f</code>?</p>

    <div class="status-panel">
      <div class="status-card">
        <div class="status-title">📁 Ruta en Disco</div>
        <div class="status-value" style="font-size: 0.95rem;">__DATA_FILE__</div>
      </div>
      <div class="status-card">
        <div class="status-title">📦 Hostname del Contenedor</div>
        <div class="status-value">__HOSTNAME__</div>
      </div>
      <div class="status-card">
        <div class="status-title">📊 Ventas Guardadas</div>
        <div class="status-value" style="color: var(--green);">__TOTAL_VENTAS__ registros</div>
      </div>
    </div>

    <div class="action-bar">
      <a href="/vender?tipo=Tinto+Campesino+con+Panela&cliente=Metro+Paisa" class="btn btn-gold">☕ + Registrar Venta de Tinto</a>
      <a href="/vender?tipo=Perico+Doble&cliente=Visitante+Medellin" class="btn btn-gold">🥛 + Registrar Venta de Perico</a>
      <a href="/api" target="_blank" class="btn btn-cyan">📡 Ver JSON Crudo</a>
    </div>

    <h3 style="margin-bottom: 0.6rem; font-size: 1rem;">📜 Registros en el archivo persistente:</h3>
    <div class="table-box">
      __TABLA_VENTAS__
    </div>
  </div>
</body>
</html>
"""

class StorageHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(url.query)

        # Endpoint para registrar nueva venta
        if url.path == "/vender":
            tipo = params.get("tipo", ["Tinto Tradicional"])[0]
            cliente = params.get("cliente", ["Cliente Mostrador"])[0]
            try:
                guardar_venta(tipo, cliente)
                # Redireccionar al inicio
                self.send_response(303)
                self.send_header("Location", "/")
                self.end_headers()
                return
            except PermissionError as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                error_resp = {
                    "error": "Error de permisos al escribir en el almacenamiento",
                    "archivo": DATA_FILE,
                    "detalle": str(e),
                    "solucion": "La carpeta montada desde el host no tiene permisos de escritura para el usuario sin privilegios del contenedor (UID 10001). Ejecuta en el host: chmod 777 mis-datos-locales"
                }
                self.wfile.write(json.dumps(error_resp, indent=2, ensure_ascii=False).encode("utf-8"))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}, indent=2).encode("utf-8"))
                return

        ventas = cargar_ventas()
        hostname = socket.gethostname()

        # Si piden JSON explícito
        accept = self.headers.get("Accept", "")
        if url.path == "/api" or ("application/json" in accept and "text/html" not in accept):
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            resp = {
                "archivo_almacenamiento": DATA_FILE,
                "hostname_contenedor_actual": hostname,
                "total_registros": len(ventas),
                "ventas": ventas
            }
            self.wfile.write(json.dumps(resp, indent=2, ensure_ascii=False).encode("utf-8"))
            return

        # Respuesta Web
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        if ventas:
            filas = []
            filas.append("<table><thead><tr><th>ID</th><th>Producto</th><th>Cliente</th><th>Fecha</th><th>Pod / Contenedor</th></tr></thead><tbody>")
            for v in reversed(ventas):
                filas.append(f"<tr><td>#{v['id']}</td><td>{v['producto']}</td><td>{v['cliente']}</td><td>{v['fecha']}</td><td><code>{v['hostname_contenedor']}</code></td></tr>")
            filas.append("</tbody></table>")
            tabla_html = "".join(filas)
        else:
            tabla_html = "<div class='empty-msg'>No hay ventas registradas aún. ¡Haz clic en los botones de arriba para registrar una!</div>"

        html = HTML_PAGE.replace("__DATA_FILE__", DATA_FILE)
        html = html.replace("__HOSTNAME__", hostname)
        html = html.replace("__TOTAL_VENTAS__", str(len(ventas)))
        html = html.replace("__TABLA_VENTAS__", tabla_html)

        self.wfile.write(html.encode("utf-8"))

    def log_message(self, formato, *args):
        sys.stdout.write(f"[{self.log_date_time_string()}] {formato % args}\n")
        sys.stdout.flush()

if __name__ == "__main__":
    server = http.server.HTTPServer(("0.0.0.0", PORT), StorageHandler)
    ventas_iniciales = len(cargar_ventas())
    print(f"💾 Servidor de Almacenamiento escuchando en http://0.0.0.0:{PORT}...")
    print(f"📁 Archivo de persistencia: {DATA_FILE} ({ventas_iniciales} ventas cargadas)")
    server.serve_forever()
