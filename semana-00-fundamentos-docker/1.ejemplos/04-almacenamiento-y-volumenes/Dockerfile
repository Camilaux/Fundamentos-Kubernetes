FROM python:3.12-alpine

# Usuario sin privilegios
RUN addgroup -g 10001 -S appgroup && \
    adduser -u 10001 -S appuser -G appgroup

WORKDIR /app

# Crear la carpeta de datos asignando permisos al usuario no-root
RUN mkdir -p /app/datos && chown -R appuser:appgroup /app/datos

COPY --chown=appuser:appgroup app.py .

ENV PORT=8080
ENV DATA_DIR="/app/datos"

USER appuser
EXPOSE 8080

CMD ["python", "app.py"]
