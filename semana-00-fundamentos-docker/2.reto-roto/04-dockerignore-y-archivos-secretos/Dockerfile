# 🚨 RETO 4 DOCKER: La fuga de secretos y contexto pesado por falta de .dockerignore 🚨
#
# Síntoma:
# 1. Al construir esta imagen:
#    docker build -t reto-leak:v1.0 semana-00-fundamentos-docker/2.reto-roto/04-dockerignore-y-archivos-secretos
# 2. Si alguien ejecuta:
#    docker run --rm reto-leak:v1.0 ls -la
#    docker run --rm reto-leak:v1.0 cat .env
#    ¡Podrá leer las claves privadas y secretos que estaban en tu máquina de desarrollo!
#
# Misión:
# 1. Crea un archivo '.dockerignore' en esta carpeta para evitar que '.env', archivos temporales
#    y carpetas de desarrollo se copien dentro de la imagen.
# 2. Corrige el 'COPY . .' en este Dockerfile para copiar únicamente los archivos necesarios.

FROM python:3.12-alpine

WORKDIR /app

RUN addgroup -g 10001 -S appgroup && \
    adduser -u 10001 -S appuser -G appgroup

# ❌ ERROR: Copia TODO el directorio de trabajo sin filtrar con .dockerignore
COPY . .

USER appuser

EXPOSE 8080

CMD ["python", "app.py"]
