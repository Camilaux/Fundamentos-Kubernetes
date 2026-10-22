# 💥 Retos Rotos de la Semana 0: Docker y su Puente a Kubernetes

¡Bienvenido al laboratorio de investigación de fallos! Aquí aprenderás a depurar los **5 errores y malas prácticas más comunes y frustrantes** que todo desarrollador enfrenta al trabajar con Docker y Kubernetes.

---

## 📑 Índice de Retos Rotos

| Reto | Tipo de Error / Tema | Nivel | Carpeta / Archivo |
| :---: | :--- | :---: | :--- |
| **01** | Proceso en segundo plano apaga el contenedor (PID 1) | 🟢 Principiante | [`01-dockerfile-roto/`](./01-dockerfile-roto) |
| **02** | Contenedor crashea por falta de variable de entorno (`ENV`) | 🟢 Principiante | [`02-variable-entorno-faltante/`](./02-variable-entorno-faltante) |
| **03** | Contenedor vulnerable ejecutándose como `root` (Seguridad) | 🟡 Intermedio | [`03-contenedor-como-root/`](./03-contenedor-como-root) |
| **04** | Fuga de contraseñas y secretos por falta de `.dockerignore` | 🟢 Principiante | [`04-dockerignore-y-archivos-secretos/`](./04-dockerignore-y-archivos-secretos) |
| **05** | Conexión rechazada por enlazar a `127.0.0.1` y puerto desalineado | 🟢 Principiante | [`05-puerto-y-host-desalineado/`](./05-puerto-y-host-desalineado) |

---

## 🎯 Reto 1: El contenedor que se apaga solo al instante (PID 1)
* **Ubicación:** [`01-dockerfile-roto/Dockerfile`](./01-dockerfile-roto/Dockerfile)
* **Nivel:** 🟢 Principiante
* **Síntoma:** Construyes la imagen con éxito (`docker build`), pero al correrla en segundo plano con `docker run -d`, el contenedor se apaga de inmediato y desaparece de `docker ps`.
* **Herramientas de investigación:**
  * `docker ps -a` (para ver el código de salida).
  * `docker logs <id-contenedor>`
* **Misión:** Modifica la instrucción `CMD` del `Dockerfile` para que el servidor Nginx corra en primer plano (*foreground*).

---

## 🎯 Reto 2: El contenedor que crashea por falta de variable de entorno
* **Ubicación:** [`02-variable-entorno-faltante/`](./02-variable-entorno-faltante)
* **Nivel:** 🟢 Principiante
* **Síntoma:** La aplicación requiere `APP_SECRET_TOKEN` para iniciar. Al hacer `docker run -d`, el contenedor termina de inmediato con `Exited (1)`.
* **Herramientas de investigación:**
  * `docker ps -a`
  * `docker logs <contenedor>`
* **Misión:** Definir un valor por defecto con `ENV` en el `Dockerfile` o pasar la variable en tiempo de ejecución con `docker run -e`.

---

## 🎯 Reto 3: El contenedor vulnerable que corre como root
* **Ubicación:** [`03-contenedor-como-root/`](./03-contenedor-como-root)
* **Nivel:** 🟡 Intermedio
* **Síntoma:** Al auditar la imagen con `docker run --rm <imagen> whoami`, responde `root` (UID 0), violando las políticas de seguridad de la organización.
* **Herramientas de investigación:**
  * `docker run --rm <imagen> whoami` o `id -u`
  * `docker inspect <contenedor> --format '{{.Config.User}}'`
* **Misión:** Crear un usuario no privilegiado (`appuser`), asignar propiedad de archivos con `--chown` y definir `USER appuser` en el `Dockerfile`.

---

## 🎯 Reto 4: La fuga de secretos por falta de `.dockerignore`
* **Ubicación:** [`04-dockerignore-y-archivos-secretos/`](./04-dockerignore-y-archivos-secretos)
* **Nivel:** 🟢 Principiante
* **Síntoma:** Un comando `COPY . .` sin `.dockerignore` empaquetó un archivo `.env` con credenciales dentro de las capas públicas de la imagen. Al hacer `docker run --rm <imagen> cat .env` se leen los secretos.
* **Herramientas de investigación:**
  * `docker run --rm <imagen> ls -la`
* **Misión:** Crear el archivo `.dockerignore` correcto y refinar la instrucción `COPY` en el `Dockerfile`.

---

## 🎯 Reto 5: El puerto fantasma y la trampa del localhost (`127.0.0.1` vs `0.0.0.0`)
* **Ubicación:** [`05-puerto-y-host-desalineado/`](./05-puerto-y-host-desalineado)
* **Nivel:** 🟢 Principiante
* **Síntoma:** `docker ps` muestra el contenedor en estado `Up`, pero al abrir `http://localhost:8080` o hacer `curl http://localhost:8080` el servidor responde `Connection refused` o `Empty reply from server`.
* **Herramientas de investigación:**
  * `docker logs <contenedor>`
  * Revisar la IP de enlace en el código fuente (`127.0.0.1` rechaza conexiones de fuera del contenedor).
* **Misión:** Corregir el código para escuchar en `0.0.0.0` y alinear los puertos entre la aplicación, el `Dockerfile` y el comando `docker run`.

---

## 🏆 ¿Cómo enviar tu solución?
1. Corrige los archivos en tu máquina.
2. Cópialos a `aportes-comunidad/soluciones-retos/tu-usuario/semana-00/` con un comentario explicando qué causaba la falla.
3. Envía tu **Pull Request** siguiendo la guía de [`CONTRIBUTING.md`](../../CONTRIBUTING.md) para subir de rango en [`ASISTENTES.md`](../../ASISTENTES.md).

