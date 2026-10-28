# 🚨 RETO 2 DOCKER: El contenedor que se apaga por falta de variable de entorno (ENV) 🚨
#
# Síntoma:
# 1. Haces 'docker build -t reto-docker-02 semana-00-fundamentos-docker/2.reto-roto/02-variable-entorno-faltante'
# 2. Corres el contenedor con 'docker run -d -p 8080:8080 --name mi-api-02 reto-docker-02'
# 3. Al hacer 'docker ps', ¡el contenedor NO está corriendo!
# 4. Al hacer 'docker ps -a' ves 'Exited (1)'.
# 5. Al hacer 'docker logs mi-api-02' verás el error:
#    "ERROR FATAL: La variable de entorno obligatoria 'APP_SECRET_TOKEN' no fue proporcionada."
#
# Pista:
# En Docker puedes solucionar esto de dos formas:
# Opción A: Declarar un valor por defecto en este Dockerfile usando la instrucción 'ENV APP_SECRET_TOKEN=...'.
# Opción B: Pasarle la variable en tiempo de ejecución con 'docker run -e APP_SECRET_TOKEN="mi-valor" ...'.

FROM python:3.12-alpine

WORKDIR /app

RUN addgroup -g 10001 -S appgroup && \
    adduser -u 10001 -S appuser -G appgroup

COPY --chown=appuser:appgroup app.py .

# ❌ ERROR: Falta definir la variable de entorno obligatoria requerida por app.py
# ENV APP_SECRET_TOKEN=...

USER appuser

EXPOSE 8080

CMD ["python", "app.py"]
