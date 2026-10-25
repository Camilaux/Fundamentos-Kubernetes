"""
Microservicio Cliente: Carrito Estación San Antonio.
Se comunica con el backend 'greca-central' usando el DNS interno de Docker.
Expone su propia interfaz en el puerto 8081 para los usuarios del Metro.
"""
import http.server
import json
import os
import socket
import sys
import urllib.error
import urllib.request

PORT = int(os.environ.get("PORT", 8081))
BACKEND_HOST = os.environ.get("BACKEND_HOST", "greca-central")
BACKEND_PORT = int(os.environ.get("BACKEND_PORT", 8080))
NOMBRE_CLIENTE = os.environ.get("NOMBRE_CLIENTE", "carrito-san-antonio")

HTML_PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🌐 Redes en Docker — Cloud Native Medellín</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0a0e17;
      --card-bg: rgba(18, 24, 38, 0.9);
      --border: rgba(6, 182, 212, 0.25);
      --cyan: #06b6d4;
      --green: #10b981;
      --gold: #f59e0b;
      --red: #ef4444;
      --text: #f9fafb;
      --muted: #9ca3af;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Outfit', sans-serif;
      background: radial-gradient(circle at 50% 10%, rgba(6, 182, 212, 0.15), transparent 45%), var(--bg);
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
      background: rgba(6, 182, 212, 0.15);
      color: var(--cyan);
      border: 1px solid var(--cyan);
      padding: 0.35rem 0.85rem;
      border-radius: 9999px;
      font-size: 0.82rem;
      font-weight: 600;
      margin-bottom: 1.2rem;
    }
    h1 { font-size: 2.2rem; margin-bottom: 0.5rem; }
    p.lead { color: var(--muted); margin-bottom: 1.5rem; }
    .network-flow {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      background: rgba(0,0,0,0.3);
      padding: 1.5rem;
      border-radius: 16px;
      margin-bottom: 1.8rem;
      flex-wrap: wrap;
    }
    .node {
      background: rgba(255,255,255,0.05);
      border: 1px solid rgba(255,255,255,0.1);
      padding: 1rem 1.2rem;
      border-radius: 12px;
      text-align: center;
      flex: 1;
      min-width: 160px;
    }
    .node-title { font-size: 0.75rem; text-transform: uppercase; color: var(--gold); margin-bottom: 0.3rem; }
    .node-name { font-size: 1.1rem; font-weight: 700; }
    .node-ip { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: var(--cyan); }
    .arrow { font-size: 1.5rem; color: var(--cyan); }
    .response-box {
      background: #030712;
      border: 1px solid rgba(255,255,255,0.1);
      border-radius: 14px;
      padding: 1.2rem;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.85rem;
      color: #38bdf8;
      overflow-x: auto;
    }
    .btn {
      display: inline-block;
      margin-top: 1.2rem;
      background: linear-gradient(135deg, var(--cyan), #0284c7);
      color: #fff;
      font-weight: 600;
      padding: 0.75rem 1.4rem;
      border-radius: 10px;
      text-decoration: none;
      transition: transform 0.2s;
    }
    .btn:hover { transform: translateY(-2px); }
  </style>
</head>
<body>
  <div class="container">
    <span class="badge">🌐 Redes Bridge en Docker • DNS Interno</span>
    <h1>Comunicación entre Contenedores</h1>
    <p class="lead">Demostración práctica: un contenedor cliente llama a un contenedor backend sin usar <code>localhost</code> ni exponer puertos externos.</p>
    
    <div class="network-flow">
      <div class="node">
        <div class="node-title">Contenedor Origen (Cliente)</div>
        <div class="node-name">__NOMBRE_CLIENTE__</div>
        <div class="node-ip">IP: __IP_CLIENTE__</div>
      </div>
      <div class="arrow">➔ [DNS: __BACKEND_HOST__] ➔</div>
      <div class="node">
        <div class="node-title">Contenedor Destino (Backend)</div>
        <div class="node-name">__BACKEND_HOST__</div>
        <div class="node-ip">IP: __IP_BACKEND_RESUELTA__</div>
      </div>
    </div>

    <h3 style="margin-bottom: 0.6rem; font-size: 1rem;">📦 Respuesta recibida desde el Backend a través de la Red:</h3>
    <pre class="response-box"><code>__RESPUESTA_JSON__</code></pre>

    <a href="/" class="btn">🔄 Hacer otra petición interna</a>
  </div>
</body>
</html>
"""

def consultar_backend():
    url = f"http://{BACKEND_HOST}:{BACKEND_PORT}/despachar-tinto"
    ip_resuelta = "No resuelta"
    try:
        ip_resuelta = socket.gethostbyname(BACKEND_HOST)
    except Exception as e:
        ip_resuelta = f"Error DNS: {e}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "carrito-san-antonio-client/1.0"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = resp.read().decode("utf-8")
            return json.loads(data), ip_resuelta, True
    except urllib.error.URLError as e:
        return {
            "error": "No se pudo conectar al backend",
            "motivo": str(e.reason),
            "pista": "¿Están ambos contenedores en la misma red Docker con 'docker network create'?"
        }, ip_resuelta, False
    except Exception as e:
        return {"error": str(e)}, ip_resuelta, False

class ClienteHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        backend_data, ip_resuelta, exito = consultar_backend()
        mi_ip = socket.gethostbyname(socket.gethostname())

        accept = self.headers.get("Accept", "")
        if "text/html" in accept:
            self.send_response(200 if exito else 503)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            html = HTML_PAGE.replace("__NOMBRE_CLIENTE__", NOMBRE_CLIENTE)
            html = html.replace("__IP_CLIENTE__", mi_ip)
            html = html.replace("__BACKEND_HOST__", BACKEND_HOST)
            html = html.replace("__IP_BACKEND_RESUELTA__", ip_resuelta)
            html = html.replace("__RESPUESTA_JSON__", json.dumps(backend_data, indent=2, ensure_ascii=False))
            self.wfile.write(html.encode("utf-8"))
        else:
            self.send_response(200 if exito else 503)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            resp = {
                "cliente": NOMBRE_CLIENTE,
                "ip_cliente": mi_ip,
                "host_consultado": BACKEND_HOST,
                "ip_resuelta_por_dns_docker": ip_resuelta,
                "respuesta_backend": backend_data
            }
            self.wfile.write(json.dumps(resp, indent=2, ensure_ascii=False).encode("utf-8"))

    def log_message(self, formato, *args):
        sys.stdout.write(f"[{self.log_date_time_string()}] {formato % args}\n")
        sys.stdout.flush()

if __name__ == "__main__":
    server = http.server.HTTPServer(("0.0.0.0", PORT), ClienteHandler)
    mi_ip = socket.gethostbyname(socket.gethostname())
    print(f"🚊 Cliente [{NOMBRE_CLIENTE}] escuchando en http://0.0.0.0:{PORT} (IP: {mi_ip})...")
    print(f"🎯 Conectándose hacia: http://{BACKEND_HOST}:{BACKEND_PORT}")
    server.serve_forever()
