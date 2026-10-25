# ☕ Ejemplo 02: API REST en Python con Buenas Prácticas de Producción

En este laboratorio aprenderás a empaquetar un microservicio en Python aplicando las **mejores prácticas de seguridad para producción y Kubernetes**: ejecución con usuario sin privilegios (*non-root*), parametrización con variables de entorno (`ENV`), limpieza de contexto con `.dockerignore` y gestión de procesos PID 1.

Además, la aplicación incluye una **interfaz web interactiva animada** con la taza de tinto paisa humeando en tiempo real y respuesta dual en JSON para llamadas con `curl`.

---

## ☕ La Analogía Paisa: La Greca del Tinto y la Receta Parametrizada

En Medellín, el buen café no se prepara a ojo:
* **El código (`app.py`):** Los granos de café seleccionados.
* **El `Dockerfile`:** La receta estandarizada de preparación.
* **El usuario no-root (`appuser`):** La persona que prepara el café tiene su carnet y uniforme de trabajo; no necesita tener las llaves maestras de toda la estación del Metro (`root`) para servir un buen tinto.
* **Las variables de entorno (`ENV MENSAJE`):** El letrero intercambiable del carrito. Puedes cambiar el letrero de *"¡Tinto recién colado!"* a *"¡Tinto campesino con panela!"* en un segundo sin tener que volver a comprar otra greca.

---

## 🛡️ Buenas Prácticas de Seguridad Implementadas

| Buena Práctica | ¿Por qué es obligatoria? | Cómo se aplica en el `Dockerfile` |
| :--- | :--- | :--- |
| **1. Principio de Menor Privilegio (Least Privilege)** | Correr como `root` (UID 0) es un riesgo crítico. Si la app es vulnerada, el atacante podría tomar control del nodo en Kubernetes. | `RUN addgroup -g 10001 -S appgroup && adduser -u 10001 -S appuser -G appgroup`<br>`USER appuser` |
| **2. Propiedad de Archivos (`--chown`)** | Evita que los archivos pertenezcan a `root` y el usuario sin privilegios no pueda leerlos. | `COPY --chown=appuser:appgroup app.py .` |
| **3. Contexto Limpio (`.dockerignore`)** | Evita subir archivos innecesarios o sensibles (`.env`, `.git/`, cachés `__pycache__`). | Archivo `.dockerignore` configurado en la raíz de la app. |
| **4. Imágenes base oficiales y ligeras** | Reduce la superficie de ataque y el tiempo de descarga. | `FROM python:3.12-alpine` (~50MB). |
| **5. Forma Exec en `CMD`** | Permite que Python reciba señales del sistema operativo (`SIGTERM`) para apagarse limpiamente. | `CMD ["python", "app.py"]` (con corchetes). |

---

## 📄 Estructura del Ejemplo

```text
02-app-python-api/
├── .dockerignore    # Archivos excluidos del build de Docker
├── Dockerfile       # Receta con usuario no-root y variables de entorno
├── app.py           # Servidor HTTP con UI web animada y API JSON dual
└── README.md        # Esta guía paso a paso
```

---

## 🚀 Flujo Práctico Paso a Paso

### 1. Construir la imagen de la API
Desde la raíz del repositorio ejecuta:

```bash
docker build -t mi-api-cnm:v1.0 semana-00-fundamentos-docker/1.ejemplos/02-app-python-api
```

Verifica la imagen creada:
```bash
docker images | grep mi-api-cnm
```

---

### 2. Ejecutar el contenedor en segundo plano
Corre el contenedor mapeando el puerto `8080`:

```bash
docker run -d -p 8080:8080 --name test-docker mi-api-cnm:v1.0
```

Verifica que esté activo:
```bash
docker ps
```

---

### 3. Probar la aplicación: Navegador vs. Terminal

* **🌐 Opción A (Experiencia Interactiva en Navegador):**  
  Abre **[http://localhost:8080](http://localhost:8080)**. Verás la taza de tinto con vapor humeante en CSS, podrás hacer clic en *"¡Colar otro Tinto!"* con sonido de vertido y usar el simulador de variables de entorno en vivo.

* **📡 Opción B (Llamada REST con `curl`):**  
  Ejecuta en tu terminal:
  ```bash
  curl http://localhost:8080
  ```

  Observa la respuesta JSON estructurada:
  ```json
  {
    "mensaje": "¡Tinto recién colado! ☕",
    "comunidad": "Cloud Native Medellín 🏔️☕",
    "workshop": "De Cero a Capitán en Kubernetes",
    "hostname_o_pod": "test-docker",
    "puerto": 8080,
    "usuario_proceso": "appuser (UID: 10001)",
    "es_root": false,
    "tintos_servidos": 1,
    "orquestador": "Listo para correr en Kubernetes"
  }
  ```
  > 🛡️ **Comprobación de Seguridad:** Fíjate en `"es_root": false` y `"usuario_proceso": "appuser (UID: 10001)"`. ¡El proceso está totalmente protegido!

---

### 4. Probar el endpoint de salud (/health)
Kubernetes utiliza estos endpoints para saber si tu aplicación está viva (*Liveness Probe*) y lista para recibir tráfico (*Readiness Probe*):

```bash
curl http://localhost:8080/health
```

Respuesta:
```json
{
  "status": "ok",
  "saludable": true,
  "uptime_segundos": 45
}
```

---

### 5. Entrar a inspeccionar el contenedor con `docker exec`
Abre una terminal dentro del contenedor para verificar los permisos del usuario:

```bash
docker exec -it test-docker sh
```
Dentro del contenedor ejecuta:
```sh
whoami    # Responderá: appuser
id        # UID 10001(appuser) GID 10001(appgroup)
exit
```

---

### 6. Sobrescribir variables de entorno en tiempo de ejecución con `-e`
Una gran ventaja de los contenedores es que puedes cambiar su comportamiento sin volver a compilar la imagen:

```bash
docker run -d -p 8081:8080 -e MENSAJE="¡Saludos desde el Poblado en Medellín! ☕" --name test-docker-env mi-api-cnm:v1.0
curl http://localhost:8081
```

### 7. Escaneo de Seguridad con Trivy (CLI)
Antes de llevar este microservicio a un clúster de Kubernetes, audita la imagen y el `Dockerfile` directamente desde tu terminal utilizando el paquete `trivy`:

```bash
# 1. Escanear vulnerabilidades conocidas (CVEs) en la imagen:
trivy image --severity HIGH,CRITICAL mi-api-cnm:v1.0

# 2. Auditar buenas prácticas y seguridad en la configuración del Dockerfile:
trivy config semana-00-fundamentos-docker/1.ejemplos/02-app-python-api

# Alternativa mediante contenedor efímero (si no tienes el paquete instalado en tu host):
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image --severity HIGH,CRITICAL mi-api-cnm:v1.0
```

> 🛡️ **Resultado de la auditoría:**
> * Al usar `python:3.12-alpine`, la imagen no contiene CVEs críticos ni altos conocidos.
> * Al configurar el usuario sin privilegios `appuser` (UID: 10001), `trivy config` aprobará la validación de *non-root container execution*.
> * Consulta la [Guía de Seguridad con Trivy](../../../recursos/guia-trivy-seguridad.md) para más opciones avanzadas.

---

### 8. Limpieza
Detén y elimina los contenedores de prueba:

```bash
docker rm -f test-docker test-docker-env
```

---

## 🌉 El Puente a Kubernetes: ¿Cómo se traduce esto?

| En Docker | En Kubernetes |
| :--- | :--- |
| `ENV MENSAJE="..."` en `Dockerfile` | Valores por defecto del contenedor. |
| `docker run -e MENSAJE="..."` | Inyección de variables con **`ConfigMap`** o **`Secret`** en el Pod. |
| `USER appuser` (UID 10001) | **`securityContext: runAsNonRoot: true`** y `runAsUser: 10001`. |
| Endpoint `/health` | **`livenessProbe`** y **`readinessProbe`** en la especificación del Pod. |
