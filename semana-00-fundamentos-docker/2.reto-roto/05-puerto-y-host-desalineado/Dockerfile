# 🚨 RETO 5 DOCKER: El puerto fantasma y la trampa del localhost (127.0.0.1 vs 0.0.0.0) 🚨
#
# Síntoma:
# 1. Construyes la imagen:
#    docker build -t reto-puerto:v1.0 semana-00-fundamentos-docker/2.reto-roto/05-puerto-y-host-desalineado
# 2. Corres el contenedor:
#    docker run -d -p 8080:8080 --name reto-puerto-app reto-puerto:v1.0
# 3. 'docker ps' dice que está "Up" (corriendo sin errores).
# 4. Sin embargo, al hacer 'curl http://localhost:8080' o abrirlo en tu navegador:
#    ¡Conexión rechazada o respuesta vacía! (Empty reply / Connection reset)
#
# Pista 1: Revisa en 'app.py' en qué dirección IP está escuchando el servidor.
#          ¿Está en '127.0.0.1' o en '0.0.0.0'?
#          (En Docker, '127.0.0.1' es el loopback interno y rechaza tráfico de fuera del contenedor).
# Pista 2: Revisa en qué puerto está escuchando 'app.py' y qué puerto mapea Docker.

FROM python:3.12-alpine

WORKDIR /app

RUN addgroup -g 10001 -S appgroup && \
    adduser -u 10001 -S appuser -G appgroup

COPY --chown=appuser:appgroup app.py .

USER appuser

# ❌ Pista: ¿El puerto aquí y en app.py coinciden?
EXPOSE 8080

CMD ["python", "app.py"]
