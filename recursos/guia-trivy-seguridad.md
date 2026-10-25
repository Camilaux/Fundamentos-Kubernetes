# 🛡️ Guía Completa de Seguridad y Escaneo de Contenedores con Trivy

**Trivy** (desarrollado por Aqua Security) es el escáner de seguridad de código abierto más popular y confiable del ecosistema Cloud Native. Es rápido, ligero y detecta:

1. **Vulnerabilidades en paquetes del SO (CVEs):** Debian, Ubuntu, Alpine, RedHat, etc.
2. **Vulnerabilidades en dependencias de código:** Python (`requirements.txt`), Node.js (`package.json`), Go, Java, etc.
3. **Malas configuraciones (IaC):** Errores de seguridad en `Dockerfile` (ej: correr como root, puertos inseguros).
4. **Fuga de secretos:** Detección de contraseñas, llaves privadas y tokens API expuestos.

---

## ⚖️ ¿Cuál es la mejor forma de usarlo: CLI vs. Servidor Web?

Una pregunta frecuente es si conviene levantarlo como un servicio web con interfaz o usarlo por línea de comandos (CLI).

| Criterio | 💻 Por Línea de Comandos (CLI / `docker run`) ⭐ **(Recomendada)** | 🌐 Servidor Web Permanente / UI |
| :--- | :--- | :--- |
| **Velocidad** | ⚡ **Instantáneo:** Escanea en 3-5 segundos y muestra los resultados de inmediato en la terminal. | ⏳ Lento: Requiere levantar contenedores, bases de datos y esperar sincronización. |
| **Consumo de Recursos** | 🟢 **Cero impacto:** El proceso corre, entrega el resultado y se apaga liberando toda la memoria. | 🔴 Alto: Consume RAM y CPU constante en segundo plano. |
| **Integración CI/CD** | 🚀 **Nativa:** Devuelve códigos de salida (`--exit-code 1`) para bloquear compilaciones con fallos críticos. | ❌ Complejo para pipelines automáticos en GitHub Actions o GitLab. |
| **Reportes Visuales** | 📊 **Soportado:** Puedes generar un archivo `.html` interactivo y abrirlo en tu navegador cuando lo necesites. | 📊 Disponible en interfaz web. |

> [!TIP]
> 🏆 **El Flujo Ideal en la Industria:**  
> 1. **Día a día:** Usa el **CLI** para escanear en segundos tus imágenes mientras desarrollas.  
> 2. **Para auditorías o gerencia:** Genera un **reporte HTML interactivo** con una sola bandera (`--template "@contrib/html.tpl" -o reporte.html`) y ábrelo en tu navegador.  
> 3. **En Kubernetes (Producción):** Se utiliza el operador **Trivy Operator** (que veremos en la Semana 6) para vigilar el clúster automáticamente.

---

## 📥 Métodos de Instalación

### Método 1: Sin Instalar Nada (Usando el Contenedor Oficial de Docker) ⭐
No necesitas instalar ningún binario en tu máquina. Solo usa la imagen oficial de Trivy montando el socket de Docker:

```bash
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $HOME/.cache/trivy:/root/.cache/ \
  aquasec/trivy:latest image <nombre-imagen>:<tag>
```

---

### Método 2: Instalación Nativa en macOS (Con Homebrew)
Es la opción más cómoda para desarrolladores de Mac:

```bash
brew install trivy
```

Verifica la instalación:
```bash
trivy --version
```

---

### Método 3: Instalación en Linux / WSL (Ubuntu, Debian)
```bash
sudo apt-get install wget apt-transport-https gnupg
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | gpg --dearmor | sudo tee /usr/share/keyrings/trivy.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb generic main" | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy
```

---

## 🛠️ Comandos Esenciales de Trivy

### 1. Escaneo Básico de una Imagen Local
Escanea todas las vulnerabilidades de la imagen construida en tu máquina:

```bash
trivy image mi-api-cnm:v1.0
```

---

### 2. Filtrar solo Vulnerabilidades Críticas y Altas
En proyectos reales, enfócate primero en lo peligroso:

```bash
trivy image --severity HIGH,CRITICAL mi-api-cnm:v1.0
```

---

### 3. Mostrar únicamente vulnerabilidades con solución disponible (`--ignore-unfixed`)
Evita el ruido de vulnerabilidades que aún no tienen parche del fabricante:

```bash
trivy image --ignore-unfixed --severity HIGH,CRITICAL mi-api-cnm:v1.0
```

---

### 4. Generar un Reporte Web HTML Interactivo
¡Esta es la mejor manera de ver los resultados en el navegador sin instalar ningún servidor web!

```bash
# Con Trivy instalado:
trivy image --format template --template "@contrib/html.tpl" -o reporte-seguridad.html mi-api-cnm:v1.0

# O usando Docker directamente:
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$(pwd)":/salida \
  aquasec/trivy:latest image \
  --format template --template "@contrib/html.tpl" \
  -o /salida/reporte-seguridad.html mi-api-cnm:v1.0

# Abrir el reporte en tu navegador (macOS):
open reporte-seguridad.html
```

---

### 5. Auditar el `Dockerfile` en busca de Malas Configuraciones
Trivy analiza las instrucciones de tu `Dockerfile` antes de construir la imagen (detecta si falta `USER`, si usas `:latest`, etc.):

```bash
trivy config semana-00-fundamentos-docker/1.ejemplos/02-app-python-api/Dockerfile
```

---

### 6. Usar Trivy como Puerta de Calidad en CI/CD (`--exit-code 1`)
Si encuentra una vulnerabilidad crítica, el comando termina con código de error `1`, fallando el pipeline de GitHub Actions o GitLab CI:

```bash
trivy image --exit-code 1 --severity CRITICAL mi-api-cnm:v1.0
```

---

## ☕ El Experimento Paisa: ¿Por qué usamos Alpine Linux?

Prueba la diferencia radical de escanear una imagen basada en Debian estándar versus una imagen minimalista en Alpine:

```bash
# 1. Escanear imagen pesada (Debian Bookworm ~1 GB)
trivy image --severity HIGH,CRITICAL python:3.12

# 2. Escanear imagen minimalista (Alpine Linux ~50 MB)
trivy image --severity HIGH,CRITICAL python:3.12-alpine
```

| Imagen | Tamaño en Disco | Vulnerabilidades Críticas | Superficie de Ataque |
| :--- | :---: | :---: | :--- |
| `python:3.12` | ~1.0 GB | 15 - 30+ CVEs | 🔴 Alta (cientos de binarios del SO innecesarios) |
| `python:3.12-alpine` | ~50 MB | **0 CVEs** | 🟢 Mínima (solo el kernel mínimo y Python) |

¡Este simple escaneo le demuestra a cualquier equipo por qué las buenas prácticas de la Semana 0 son indispensables para Kubernetes!
