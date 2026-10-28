"""
Servidor HTTP en Python sin dependencias externas (Standard Library).
Ideal para entender cómo empaquetar una aplicación con variables de entorno
y probarla primero en Docker y luego en Kubernetes.

Características:
- 🌐 Interfaz Web interactiva, animada y moderna para navegadores con la taza de tinto paisa humeante.
- 📡 Endpoint REST JSON para llamadas con curl, scripts y Kubernetes.
- 🩺 Endpoint de salud /health para probes de Kubernetes (Liveness y Readiness).
- 🛡️ Inspección de seguridad en tiempo de ejecución (UID / usuario no-root).
"""
import http.server
import json
import os
import socket
import sys
import time
import urllib.parse

# 1. Variables de entorno configurables
PORT = int(os.environ.get("PORT", 8080))
MENSAJE_DEFAULT = os.environ.get("MENSAJE", "¡Tinto recién colado! ☕")
COMUNIDAD = "Cloud Native Medellín 🏔️☕"
WORKSHOP = "De Cero a Capitán en Kubernetes"

START_TIME = time.time()
TINTOS_TOTALES = 1

# 2. Plantilla HTML interactiva con diseño moderno, animaciones CSS y Web Audio API
HTML_PAGE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>☕ Cloud Native Medellín — Tinto Recién Colado</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0a0e17;
      --card-bg: rgba(18, 24, 38, 0.88);
      --card-border: rgba(245, 158, 11, 0.25);
      --coffee-gold: #f59e0b;
      --coffee-warm: #d97706;
      --coffee-dark: #78350f;
      --accent-cyan: #06b6d4;
      --accent-green: #10b981;
      --accent-red: #ef4444;
      --text-main: #f9fafb;
      --text-muted: #9ca3af;
      --code-bg: #030712;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: 'Outfit', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: radial-gradient(circle at 50% 15%, rgba(217, 119, 6, 0.18), transparent 45%),
                  radial-gradient(circle at 85% 85%, rgba(6, 182, 212, 0.1), transparent 40%),
                  var(--bg);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 2rem 1rem;
      overflow-x: hidden;
    }

    .container {
      width: 100%;
      max-width: 840px;
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      backdrop-filter: blur(24px);
      -webkit-backdrop-filter: blur(24px);
      border-radius: 28px;
      padding: 2.8rem 2.2rem;
      box-shadow: 0 30px 70px -15px rgba(0, 0, 0, 0.75),
                  0 0 40px -5px rgba(245, 158, 11, 0.18);
      position: relative;
      animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1);
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(24px) scale(0.98); }
      to { opacity: 1; transform: translateY(0) scale(1); }
    }

    /* Badges Bar */
    .badge-bar {
      display: flex;
      flex-wrap: wrap;
      gap: 0.6rem;
      justify-content: center;
      margin-bottom: 1.5rem;
    }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      padding: 0.4rem 0.95rem;
      border-radius: 9999px;
      font-size: 0.82rem;
      font-weight: 600;
      letter-spacing: 0.3px;
      border: 1px solid transparent;
      transition: all 0.25s ease;
    }

    .badge-coffee {
      background: rgba(245, 158, 11, 0.15);
      color: var(--coffee-gold);
      border-color: rgba(245, 158, 11, 0.4);
    }

    .badge-cyan {
      background: rgba(6, 182, 212, 0.15);
      color: var(--accent-cyan);
      border-color: rgba(6, 182, 212, 0.4);
    }

    .badge-green {
      background: rgba(16, 185, 129, 0.15);
      color: var(--accent-green);
      border-color: rgba(16, 185, 129, 0.4);
    }

    .pulse-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--accent-green);
      box-shadow: 0 0 10px var(--accent-green);
      animation: pulse 1.8s infinite;
    }

    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.75); }
    }

    /* Header */
    header {
      text-align: center;
      margin-bottom: 2rem;
    }

    h1 {
      font-size: 2.3rem;
      font-weight: 800;
      line-height: 1.2;
      background: linear-gradient(135deg, #ffffff 40%, var(--coffee-gold) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 0.5rem;
    }

    .subtitle {
      font-size: 1.05rem;
      color: var(--text-muted);
    }

    /* Coffee Animation Showcase */
    .coffee-showcase {
      display: flex;
      flex-direction: column;
      align-items: center;
      margin: 1.8rem 0;
      position: relative;
    }

    .cup-wrapper {
      position: relative;
      width: 140px;
      height: 125px;
      display: flex;
      justify-content: center;
      align-items: flex-end;
      cursor: pointer;
    }

    /* Steam animation */
    .steam-container {
      position: absolute;
      top: -10px;
      display: flex;
      gap: 16px;
      z-index: 10;
    }

    .steam-wisp {
      width: 7px;
      height: 52px;
      background: linear-gradient(to top, rgba(255, 255, 255, 0.8), rgba(245, 158, 11, 0.35), transparent);
      border-radius: 50% 50% 20% 20%;
      filter: blur(3px);
      animation: steamRise 2.5s infinite ease-out;
      opacity: 0;
    }

    .steam-wisp:nth-child(1) { animation-delay: 0s; }
    .steam-wisp:nth-child(2) { animation-delay: 0.8s; height: 60px; }
    .steam-wisp:nth-child(3) { animation-delay: 1.6s; }

    @keyframes steamRise {
      0% {
        transform: translateY(20px) scaleX(0.7) skewX(0deg);
        opacity: 0;
      }
      30% {
        opacity: 0.85;
      }
      70% {
        transform: translateY(-28px) scaleX(1.5) skewX(10deg);
        opacity: 0.35;
      }
      100% {
        transform: translateY(-55px) scaleX(2.2) skewX(-12deg);
        opacity: 0;
      }
    }

    /* Coffee Cup CSS */
    .coffee-cup {
      position: relative;
      width: 112px;
      height: 74px;
      background: linear-gradient(135deg, #f9fafb 0%, #e5e7eb 65%, #9ca3af 100%);
      border-radius: 0 0 46px 46px;
      box-shadow: inset 0 -6px 12px rgba(0, 0, 0, 0.25),
                  0 10px 24px rgba(0, 0, 0, 0.45);
      z-index: 2;
      transition: transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    .coffee-cup:hover {
      transform: scale(1.04);
    }

    .cup-handle {
      position: absolute;
      right: -24px;
      top: 10px;
      width: 32px;
      height: 42px;
      border: 8px solid #f3f4f6;
      border-left: none;
      border-radius: 0 22px 22px 0;
      box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.25);
    }

    .cup-saucer {
      position: absolute;
      bottom: -7px;
      width: 142px;
      height: 14px;
      background: linear-gradient(to bottom, #f3f4f6, #9ca3af);
      border-radius: 50%;
      box-shadow: 0 8px 18px rgba(0, 0, 0, 0.55);
      z-index: 1;
    }

    .cup-liquid {
      position: absolute;
      top: 5px;
      left: 10px;
      right: 10px;
      height: 20px;
      background: radial-gradient(ellipse at center, #78350f 0%, #451a03 70%, #1f0d05 100%);
      border-radius: 50%;
      box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.9);
      overflow: hidden;
    }

    .cup-crema {
      position: absolute;
      top: 3px;
      left: 20%;
      width: 32px;
      height: 11px;
      background: rgba(245, 158, 11, 0.4);
      border-radius: 50%;
      filter: blur(2px);
      animation: cremaDrift 4s ease-in-out infinite alternate;
    }

    @keyframes cremaDrift {
      0% { transform: scale(1) translateX(0); }
      100% { transform: scale(1.2) translateX(14px); }
    }

    /* Message Callout */
    .message-hero {
      margin-top: 1.8rem;
      background: rgba(0, 0, 0, 0.4);
      border: 1px solid rgba(245, 158, 11, 0.35);
      padding: 1.25rem 2rem;
      border-radius: 18px;
      text-align: center;
      box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.5);
      max-width: 90%;
      width: 100%;
    }

    .message-label {
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      color: var(--coffee-gold);
      font-weight: 700;
      margin-bottom: 0.45rem;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.4rem;
    }

    .message-text {
      font-size: 1.55rem;
      font-weight: 700;
      color: #fff;
      text-shadow: 0 0 24px rgba(245, 158, 11, 0.55);
      transition: all 0.3s ease;
    }

    /* Counter Badge */
    .counter-pill {
      font-size: 0.88rem;
      color: var(--coffee-gold);
      background: rgba(245, 158, 11, 0.12);
      border: 1px dashed rgba(245, 158, 11, 0.35);
      padding: 0.45rem 1.2rem;
      border-radius: 9999px;
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      margin-top: 0.8rem;
    }

    /* Action Buttons */
    .actions-row {
      display: flex;
      flex-wrap: wrap;
      gap: 0.9rem;
      justify-content: center;
      margin: 1.8rem 0;
    }

    .btn {
      appearance: none;
      border: none;
      cursor: pointer;
      font-family: inherit;
      font-size: 0.95rem;
      font-weight: 600;
      padding: 0.85rem 1.6rem;
      border-radius: 14px;
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .btn-primary {
      background: linear-gradient(135deg, var(--coffee-gold), var(--coffee-warm));
      color: #0b0f19;
      box-shadow: 0 4px 18px rgba(245, 158, 11, 0.45);
    }

    .btn-primary:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 28px rgba(245, 158, 11, 0.65);
    }

    .btn-primary:active {
      transform: translateY(0);
    }

    .btn-secondary {
      background: rgba(255, 255, 255, 0.07);
      color: var(--text-main);
      border: 1px solid rgba(255, 255, 255, 0.14);
    }

    .btn-secondary:hover {
      background: rgba(255, 255, 255, 0.14);
      transform: translateY(-2px);
    }

    /* Presets Section */
    .presets-section {
      background: rgba(0, 0, 0, 0.25);
      border: 1px solid rgba(255, 255, 255, 0.07);
      border-radius: 18px;
      padding: 1.35rem;
      margin: 1.6rem 0;
    }

    .presets-title {
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--coffee-gold);
      margin-bottom: 0.85rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 0.5rem;
    }

    .preset-chips {
      display: flex;
      flex-wrap: wrap;
      gap: 0.55rem;
    }

    .chip {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: var(--text-main);
      padding: 0.45rem 0.9rem;
      border-radius: 10px;
      font-size: 0.85rem;
      cursor: pointer;
      transition: all 0.2s ease;
      font-family: inherit;
    }

    .chip:hover {
      background: rgba(245, 158, 11, 0.18);
      border-color: var(--coffee-gold);
      transform: translateY(-1px);
    }

    /* Telemetry Grid */
    .telemetry-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 1rem;
      margin: 1.8rem 0;
    }

    .telemetry-card {
      background: rgba(0, 0, 0, 0.25);
      border: 1px solid rgba(255, 255, 255, 0.07);
      border-radius: 16px;
      padding: 1.1rem 1.25rem;
      transition: all 0.25s ease;
    }

    .telemetry-card:hover {
      border-color: rgba(245, 158, 11, 0.35);
      transform: translateY(-2px);
    }

    .telemetry-title {
      font-size: 0.74rem;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.8px;
      margin-bottom: 0.4rem;
      display: flex;
      align-items: center;
      gap: 0.35rem;
    }

    .telemetry-value {
      font-family: 'JetBrains Mono', monospace;
      font-size: 1.05rem;
      font-weight: 600;
      color: #fff;
      word-break: break-all;
    }

    .safe-badge {
      color: var(--accent-green);
      display: inline-flex;
      align-items: center;
      gap: 0.3rem;
      font-size: 0.9rem;
    }

    .danger-badge {
      color: var(--accent-red);
      display: inline-flex;
      align-items: center;
      gap: 0.3rem;
      font-size: 0.9rem;
    }

    /* JSON Box */
    .json-box {
      margin-top: 1.6rem;
      background: var(--code-bg);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 16px;
      overflow: hidden;
    }

    .json-header {
      background: rgba(255, 255, 255, 0.035);
      padding: 0.7rem 1.2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid rgba(255, 255, 255, 0.07);
    }

    .json-header span {
      font-size: 0.82rem;
      font-family: 'JetBrains Mono', monospace;
      color: var(--text-muted);
    }

    .btn-copy {
      background: transparent;
      border: none;
      color: var(--coffee-gold);
      font-family: inherit;
      font-size: 0.82rem;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      padding: 0.3rem 0.65rem;
      border-radius: 8px;
      transition: background 0.2s;
    }

    .btn-copy:hover {
      background: rgba(245, 158, 11, 0.15);
    }

    pre {
      padding: 1.25rem;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.86rem;
      line-height: 1.65;
      overflow-x: auto;
    }

    pre .json-key { color: #f472b6; }
    pre .json-str { color: #34d399; }
    pre .json-num { color: #f59e0b; }
    pre .json-bool { color: #a78bfa; }

    footer {
      text-align: center;
      margin-top: 2rem;
      font-size: 0.88rem;
      color: var(--text-muted);
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      padding-top: 1.35rem;
    }

    /* Animation when pouring coffee */
    @keyframes coffeePour {
      0% { transform: scale(0.95); opacity: 0.8; }
      50% { transform: scale(1.08); opacity: 1; filter: drop-shadow(0 0 20px rgba(245, 158, 11, 0.85)); }
      100% { transform: scale(1); opacity: 1; }
    }

    .pouring {
      animation: coffeePour 0.65s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="badge-bar">
      <span class="badge badge-coffee">☕ Semana 00 • Docker</span>
      <span class="badge badge-cyan">🏔️ Cloud Native Medellín</span>
      <span class="badge badge-green"><span class="pulse-dot"></span> Pod Activo</span>
    </div>

    <header>
      <h1>¡Tinto Paisa Containerizado!</h1>
      <p class="subtitle">Workshop: De Cero a Capitán en Kubernetes</p>
    </header>

    <div class="coffee-showcase">
      <div class="cup-wrapper" id="cupWrapper" onclick="colarTinto()" title="Haz clic para colar un tinto">
        <div class="steam-container">
          <div class="steam-wisp"></div>
          <div class="steam-wisp"></div>
          <div class="steam-wisp"></div>
        </div>
        <div class="cup-saucer"></div>
        <div class="coffee-cup" id="coffeeCup">
          <div class="cup-handle"></div>
          <div class="cup-liquid">
            <div class="cup-crema"></div>
          </div>
        </div>
      </div>

      <div class="message-hero">
        <div class="message-label">☕ Variable de Entorno [ENV MENSAJE]</div>
        <div class="message-text" id="mensajeDisplay">__MENSAJE__</div>
      </div>

      <div class="counter-pill">
        <span>Tintos servidos por esta greca:</span>
        <strong id="tintosCounter" style="font-size: 1.15rem; color: #fff;">__TINTOS__</strong>
      </div>
    </div>

    <div class="actions-row">
      <button class="btn btn-primary" id="btnColar" onclick="colarTinto()">
        ☕ ¡Colar otro Tinto!
      </button>
      <button class="btn btn-secondary" onclick="probarHealth()">
        🩺 Probar /health
      </button>
      <button class="btn btn-secondary" onclick="verApiJson()">
        📡 Ver Endpoint /api
      </button>
    </div>

    <!-- Presets -->
    <div class="presets-section">
      <div class="presets-title">
        <span>🎛️ Simular Variación de Variable de Entorno:</span>
        <span style="font-size: 0.78rem; color: var(--text-muted); font-weight: 400;">Pruébalo en vivo</span>
      </div>
      <div class="preset-chips">
        <button class="chip" onclick="cambiarMensaje('¡Tinto recién colado! ☕')">☕ ¡Tinto recién colado! ☕</button>
        <button class="chip" onclick="cambiarMensaje('¡Tinto campesino con panela y canela! 🍯')">🍯 Tinto campesino con panela</button>
        <button class="chip" onclick="cambiarMensaje('¡Perico bien cargado pal frío! 🥛')">🥛 Perico bien caliente</button>
        <button class="chip" onclick="cambiarMensaje('¡Tinto caliente en el Metro San Antonio! 🚊')">🚊 Estación San Antonio</button>
        <button class="chip" onclick="cambiarMensaje('¡De Cero a Capitán en Kubernetes! ☸️🚀')">☸️ De Cero a Capitán</button>
      </div>
    </div>

    <!-- Telemetry -->
    <div class="telemetry-grid">
      <div class="telemetry-card">
        <div class="telemetry-title">📦 Hostname / Pod</div>
        <div class="telemetry-value">__HOSTNAME__</div>
      </div>

      <div class="telemetry-card">
        <div class="telemetry-title">🔌 Puerto Activo</div>
        <div class="telemetry-value">:__PUERTO__</div>
      </div>

      <div class="telemetry-card">
        <div class="telemetry-title">🛡️ Proceso Contenedor</div>
        <div class="telemetry-value" style="font-size: 0.95rem;">
          __USUARIO_BADGE__
        </div>
      </div>

      <div class="telemetry-card">
        <div class="telemetry-title">⏱️ Uptime Contenedor</div>
        <div class="telemetry-value" id="uptimeVal">0s</div>
      </div>
    </div>

    <!-- Live JSON Box -->
    <div class="json-box">
      <div class="json-header">
        <span>Respuesta Cruda de la API (JSON)</span>
        <button class="btn-copy" onclick="copiarJson()">
          <span id="copyIcon">📋</span> <span id="copyText">Copiar JSON</span>
        </button>
      </div>
      <pre><code id="jsonCode"></code></pre>
    </div>

    <footer>
      🏔️ <strong>Cloud Native Medellín</strong> • De Cero a Capitán en Kubernetes • Semana 00: Fundamentos de Docker ☕
    </footer>
  </div>

  <script>
    let tintosCount = __TINTOS__;
    let startTime = Date.now();
    let audioCtx = null;

    let payload = {
      mensaje: "__MENSAJE__",
      comunidad: "Cloud Native Medellín 🏔️☕",
      workshop: "De Cero a Capitán en Kubernetes",
      hostname_o_pod: "__HOSTNAME__",
      puerto: __PUERTO__,
      usuario_proceso: "__USUARIO__",
      es_root: __ES_ROOT__,
      tintos_servidos: __TINTOS__,
      orquestador: "Listo para correr en Kubernetes"
    };

    function renderJson() {
      const codeEl = document.getElementById("jsonCode");
      const jsonStr = JSON.stringify(payload, null, 2);
      codeEl.innerHTML = jsonStr
        .replace(/"(.*?)":/g, '<span class="json-key">"$1"</span>:')
        .replace(/:\s*"(.*?)"/g, ': <span class="json-str">"$1"</span>')
        .replace(/:\s*([0-9]+)/g, ': <span class="json-num">$1</span>')
        .replace(/:\s*(true|false)/g, ': <span class="json-bool">$1</span>');
    }

    function playCoffeeSound() {
      try {
        if (!audioCtx) {
          audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        }
        if (audioCtx.state === 'suspended') {
          audioCtx.resume();
        }
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(587.33, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(880, audioCtx.currentTime + 0.15);
        gain.gain.setValueAtTime(0.15, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.35);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.35);
      } catch (e) {}
    }

    function colarTinto() {
      tintosCount++;
      document.getElementById("tintosCounter").innerText = tintosCount;
      payload.tintos_servidos = tintosCount;
      renderJson();

      const cup = document.getElementById("coffeeCup");
      cup.classList.remove("pouring");
      void cup.offsetWidth;
      cup.classList.add("pouring");

      playCoffeeSound();

      const btn = document.getElementById("btnColar");
      const originalText = btn.innerText;
      btn.innerText = "✨ ¡Tinto Servido! ☕";
      setTimeout(() => { btn.innerText = originalText; }, 700);
    }

    function cambiarMensaje(nuevo) {
      payload.mensaje = nuevo;
      document.getElementById("mensajeDisplay").innerText = nuevo;
      renderJson();
      colarTinto();
    }

    function copiarJson() {
      navigator.clipboard.writeText(JSON.stringify(payload, null, 2)).then(() => {
        const copyText = document.getElementById("copyText");
        copyText.innerText = "¡Copiado!";
        setTimeout(() => { copyText.innerText = "Copiar JSON"; }, 2000);
      });
    }

    function probarHealth() {
      window.open('/health', '_blank');
    }

    function verApiJson() {
      window.open('/api', '_blank');
    }

    // Cronómetro de Uptime en vivo
    setInterval(() => {
      const elapsed = Math.floor((Date.now() - startTime) / 1000);
      const m = Math.floor(elapsed / 60);
      const s = elapsed % 60;
      document.getElementById("uptimeVal").innerText = m > 0 ? `${m}m ${s}s` : `${s}s`;
    }, 1000);

    renderJson();
  </script>
</body>
</html>
"""


class SimpleHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global TINTOS_TOTALES

        # 1. Endpoint de salud para Kubernetes (Liveness & Readiness probe)
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            uptime_seg = int(time.time() - START_TIME)
            self.wfile.write(json.dumps({
                "status": "ok",
                "saludable": True,
                "uptime_segundos": uptime_seg
            }, indent=2).encode("utf-8"))
            return

        # 2. Información del proceso y usuario para verificar buenas prácticas
        usuario = "desconocido"
        uid = -1
        try:
            import pwd
            uid = os.getuid()
            usuario = pwd.getpwuid(uid).pw_name
        except Exception:
            usuario = os.environ.get("USER", "appuser")

        es_root = (uid == 0)
        hostname = socket.gethostname()

        # Objeto de respuesta estándar
        respuesta = {
            "mensaje": MENSAJE_DEFAULT,
            "comunidad": COMUNIDAD,
            "workshop": WORKSHOP,
            "hostname_o_pod": hostname,
            "puerto": PORT,
            "usuario_proceso": f"{usuario} (UID: {uid})",
            "es_root": es_root,
            "tintos_servidos": TINTOS_TOTALES,
            "orquestador": "Listo para correr en Kubernetes"
        }

        # 3. Detección de cliente: Navegador Web vs. curl / API
        accept = self.headers.get("Accept", "")
        user_agent = self.headers.get("User-Agent", "")
        url_parsed = urllib.parse.urlparse(self.path)

        # Si el usuario explícitamente pide /api o ?format=json o viene de curl/wget sin pedir html:
        quiere_json = (
            url_parsed.path == "/api"
            or "format=json" in url_parsed.query
            or ("application/json" in accept and "text/html" not in accept)
            or ("curl" in user_agent.lower() and "text/html" not in accept)
        )

        if not quiere_json:
            # Respuesta interactiva y visual para navegadores
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()

            if es_root:
                badge_usuario = '<span class="danger-badge">⚠️ root (UID 0) — Inseguro</span>'
            else:
                badge_usuario = f'<span class="safe-badge">🛡️ {usuario} (UID {uid}) — Seguro</span>'

            html_renderizado = HTML_PAGE
            html_renderizado = html_renderizado.replace("__MENSAJE__", MENSAJE_DEFAULT)
            html_renderizado = html_renderizado.replace("__HOSTNAME__", hostname)
            html_renderizado = html_renderizado.replace("__PUERTO__", str(PORT))
            html_renderizado = html_renderizado.replace("__USUARIO__", f"{usuario} (UID: {uid})")
            html_renderizado = html_renderizado.replace("__USUARIO_BADGE__", badge_usuario)
            html_renderizado = html_renderizado.replace("__ES_ROOT__", "true" if es_root else "false")
            html_renderizado = html_renderizado.replace("__TINTOS__", str(TINTOS_TOTALES))

            self.wfile.write(html_renderizado.encode("utf-8"))
        else:
            # Respuesta en formato JSON para terminal, curl y APIs
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(respuesta, indent=2, ensure_ascii=False).encode("utf-8"))

    def log_message(self, formato, *args):
        # Logs formateados para docker logs y kubectl logs
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
    print(f"☕ Mensaje configurado: '{MENSAJE_DEFAULT}'")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido limpiamente.")
        servidor.server_close()
