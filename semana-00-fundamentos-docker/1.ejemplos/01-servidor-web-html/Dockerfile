# 1. Imagen base oficial y ligera basada en Alpine Linux
FROM nginx:alpine

# 2. Copiamos nuestro archivo index.html dentro de la ruta pública de Nginx
COPY index.html /usr/share/nginx/html/index.html

# 3. Documentamos que el contenedor escucha peticiones en el puerto 80
EXPOSE 80

# 4. Comando que se ejecuta al encender el contenedor (en primer plano para que no se apague)
CMD ["nginx", "-g", "daemon off;"]
