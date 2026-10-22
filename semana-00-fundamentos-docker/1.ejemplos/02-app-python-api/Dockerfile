# 1. Usamos una imagen base oficial con versión fijada (pinned tag) sobre Alpine Linux (~50MB)
FROM python:3.12-alpine

# 2. 🛡️ Buenas Prácticas de Seguridad: Crear usuario y grupo sin privilegios (Least Privilege)
# En Docker y Kubernetes, correr como 'root' (UID 0) es una mala práctica.
# Creamos el grupo y usuario 'appuser' con UID y GID 10001:
RUN addgroup -g 10001 -S appgroup && \
    adduser -u 10001 -S appuser -G appgroup

# 3. Definimos la carpeta de trabajo dentro del contenedor
WORKDIR /app

# 4. Copiamos el código asignando la propiedad directamente al usuario no-root (--chown)
COPY --chown=appuser:appgroup app.py .

# 5. Definimos variables de entorno por defecto (pueden ser sobrescritas al correr)
ENV PORT=8080
ENV MENSAJE="¡Hola desde mi contenedor en Cloud Native Medellín! 🏔️☕"

# 6. 🔒 Cambiamos al usuario sin privilegios antes del comando de inicio
# A partir de esta línea, la aplicación NO corre como root
USER appuser

# 7. Documentamos el puerto que escucha la aplicación
EXPOSE 8080

# 8. Ejecutamos la aplicación en primer plano (PID 1) usando la forma exec (corchetes)
# Esto asegura que reciba señales del sistema operativo (SIGTERM) para apagado limpio
CMD ["python", "app.py"]

