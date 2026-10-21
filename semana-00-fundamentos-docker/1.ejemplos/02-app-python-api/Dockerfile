# 1. Usamos una imagen base oficial de Python sobre Alpine Linux (ultraligera, ~50MB)
FROM python:3.12-alpine

# 2. Definimos la carpeta de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiamos el archivo de la aplicación
COPY app.py .

# 4. Definimos variables de entorno por defecto (pueden ser sobrescritas al correr)
ENV PORT=8080
ENV MENSAJE="¡Hola desde mi contenedor en Cloud Native Medellín! 🏔️☕"

# 5. Documentamos el puerto que escucha la aplicación
EXPOSE 8080

# 6. Ejecutamos la aplicación en primer plano (PID 1)
CMD ["python", "app.py"]
