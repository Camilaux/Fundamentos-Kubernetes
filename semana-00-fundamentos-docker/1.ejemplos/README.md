# 📂 Ejemplos Prácticos de Docker (Semana 0)

En esta carpeta encontrarás los laboratorios prácticos organizados modularmente para aprender a empaquetar, conectar y persistir aplicaciones con Docker antes de dar el salto a Kubernetes.

---

## 📑 Índice de Ejemplos

| Carpeta | Tipo de Aplicación | Concepto Clave | Enlace a la Guía |
| :--- | :--- | :--- | :--- |
| [`01-servidor-web-html/`](./01-servidor-web-html) | Sitio Web Estático (Nginx) | `FROM`, `COPY`, `EXPOSE` y `CMD` básico con Nginx en Alpine (~25MB). | 🔗 [Ver Laboratorio 01](./01-servidor-web-html/README.md) |
| [`02-app-python-api/`](./02-app-python-api) | API REST en Python (Microservicio) | Usuario no-root (`appuser`), `COPY --chown`, `ENV`, `.dockerignore`, PID 1 y UI interactiva. | 🔗 [Ver Laboratorio 02](./02-app-python-api/README.md) |
| [`03-redes-comunicacion-contenedores/`](./03-redes-comunicacion-contenedores) | Microservicios en Red Bridge | Redes personalizadas (`docker network create`), DNS interno por nombre y aislamiento. | 🔗 [Ver Laboratorio 03](./03-redes-comunicacion-contenedores/README.md) |
| [`04-almacenamiento-y-volumenes/`](./04-almacenamiento-y-volumenes) | API con Persistencia de Ventas | Datos efímeros vs **Named Volumes** (`docker volume`) vs **Bind Mounts** (`-v`). | 🔗 [Ver Laboratorio 04](./04-almacenamiento-y-volumenes/README.md) |

---

## 🛡️ Escaneo de Seguridad de Imágenes con Trivy

En entornos reales de Kubernetes y producción, construir la imagen es solo el primer paso. Toda imagen debe ser **auditada en busca de vulnerabilidades (CVEs)** y malas configuraciones antes de desplegarse.

Para esto usamos **Trivy**, el escáner de seguridad estándar de la industria Cloud Native.

> 📖 **Guía Completa:** Puedes consultar todos los comandos y detalles en [**Guía de Seguridad con Trivy**](../../recursos/guia-trivy-seguridad.md).

---

### 1. ¿Cómo ejecutar Trivy?

Tienes dos opciones excelentes:

#### Opción A: Sin instalar nada (Usando el contenedor oficial de Docker) ⭐
No necesitas instalar binarios en tu máquina. Ejecuta Trivy directamente como un contenedor efímero:

```bash
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $HOME/.cache/trivy:/root/.cache/ \
  aquasec/trivy:latest image <nombre-imagen>:<tag>
```

#### Opción B: Instalación nativa por CLI (macOS con Homebrew)
```bash
brew install trivy
```

---

### 2. Escaneo en Terminal (CLI) — La forma más rápida y recomendada

Escanea las imágenes construidas en los ejemplos:

```bash
# 1. Escanear la API de Python (Ejemplo 02)
trivy image --severity HIGH,CRITICAL mi-api-cnm:v1.0

# 2. Escanear el servidor web Nginx (Ejemplo 01)
trivy image --severity HIGH,CRITICAL mi-web-estatica:v1.0

# 3. Escanear ignorando vulnerabilidades sin parche disponible
trivy image --ignore-unfixed --severity HIGH,CRITICAL mi-api-cnm:v1.0
```

---

### 3. Generar Reporte Visual en la Web (HTML Interactivo)

Si prefieres ver los resultados en tu **navegador web** en lugar de la terminal, Trivy permite exportar un reporte interactivo en formato HTML:

```bash
# Con Trivy instalado nativamente:
trivy image --format template --template "@contrib/html.tpl" -o reporte-seguridad.html mi-api-cnm:v1.0
open reporte-seguridad.html

# O ejecutándolo directamente con Docker:
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$(pwd)":/salida \
  aquasec/trivy:latest image \
  --format template --template "@contrib/html.tpl" \
  -o /salida/reporte-seguridad.html mi-api-cnm:v1.0
open reporte-seguridad.html
```

> **¿Qué verás en la web?** Una página moderna e interactiva con el resumen de severidades (Total de vulnerabilidades, Críticas, Altas, Medias), listado de paquetes afectados, links directos a las bases de datos de CVEs y la versión exacta que corrige el fallo (*Fixed Version*).

---

### 4. Auditar el `Dockerfile` antes de construir (IaC Misconfigurations)
Trivy también analiza el archivo `Dockerfile` para alertarte si olvidaste definir un usuario no-root o si dejaste configuraciones inseguras:

```bash
trivy config semana-00-fundamentos-docker/1.ejemplos/02-app-python-api/Dockerfile
```

---

> [!TIP]
> 👉 **¿Cuándo entra Kubernetes?**  
> En la **Semana 1** aprenderás a instalar tu clúster local con **Kind** y a orquestar contenedores usando Pods, Services y Deployments.
