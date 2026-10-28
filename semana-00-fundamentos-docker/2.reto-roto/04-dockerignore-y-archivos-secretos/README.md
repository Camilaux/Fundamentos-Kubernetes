# 🎯 Reto 4: La fuga de secretos y contexto pesado por falta de `.dockerignore`

* **Dificultad:** 🟢 Principiante / 🟡 Intermedio
* **Archivos:** [`Dockerfile`](./Dockerfile) y [`.env`](./.env)

---

## 🔍 El Escenario

Un desarrollador del equipo usó `COPY . .` en el `Dockerfile` pero olvidó crear el archivo `.dockerignore`. En su máquina local tenía un archivo `.env` con credenciales de base de datos y llaves de acceso de prueba.

Al publicar la imagen a un registro público de contenedores, ¡cualquiera con acceso a la imagen puede inspeccionar sus capas y robar las contraseñas!

### 💥 Síntoma

1. Construye la imagen actual:
   ```bash
   docker build -t reto-leak:v1.0 semana-00-fundamentos-docker/2.reto-roto/04-dockerignore-y-archivos-secretos
   ```
2. Inspecciona el interior del contenedor:
   ```bash
   docker run --rm reto-leak:v1.0 cat .env
   ```
   *Salida:* ¡Podrás ver todas las contraseñas en texto plano! 😱

---

## 🎯 Tu Misión

1. Crea el archivo `.dockerignore` en `semana-00-fundamentos-docker/2.reto-roto/04-dockerignore-y-archivos-secretos/` para excluir:
   * `.env`
   * `*.log`
   * `*.tmp`
   * `.git/`
   * `README.md`
2. Modifica el [`Dockerfile`](./Dockerfile) para copiar de manera explícita solo el archivo `app.py` asignando la propiedad con `--chown=appuser:appgroup`.
3. Vuelve a construir la imagen:
   ```bash
   docker build -t reto-leak:v1.0 semana-00-fundamentos-docker/2.reto-roto/04-dockerignore-y-archivos-secretos
   ```
4. Comprueba que el archivo ya no exista dentro de la imagen:
   ```bash
   docker run --rm reto-leak:v1.0 ls -la
   ```
   Y al probar `docker run --rm reto-leak:v1.0 cat .env`, Docker debe responder:
   `cat: can't open '.env': No such file or directory` ✅
