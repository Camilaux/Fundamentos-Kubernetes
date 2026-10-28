# 🌐 Ejemplo 01: Servidor Web Estático con Nginx

En este primer laboratorio aprenderás las directivas más fundamentales de Docker: `FROM`, `COPY`, `EXPOSE` y `CMD`, empaquetando una página web HTML servida por **Nginx** sobre **Alpine Linux**.

---

## ☕ La Analogía Paisa: El Aviso del Carrito de Tintos

Imagina que acabas de diseñar un cartel publicitario para tu carrito de tintos en la Estación San Antonio (`index.html`).
* **`FROM nginx:alpine`:** Compras un soporte ligero y estándar de exhibición ya fabricado en la tienda (la imagen oficial de Nginx en Alpine Linux, que pesa menos de ~25MB).
* **`COPY index.html ...`:** Pegas tu cartel dentro del mostrador de exhibición de Nginx (`/usr/share/nginx/html/`).
* **`EXPOSE 80`:** Dejas visible la ventanilla donde se atiende al público (puerto HTTP estándar 80).
* **`CMD ["nginx", "-g", "daemon off;"]`:** Enciendes el mostrador y te quedas atendiendo en primer plano para que el puesto no se cierre.

---

## 📄 Estructura del Ejemplo

```text
01-servidor-web-html/
├── Dockerfile      # Receta para construir la imagen con Nginx
├── index.html      # Página web con diseño estilizado de Cloud Native Medellín
└── README.md       # Esta guía paso a paso
```

---

## 🚀 Flujo Práctico Paso a Paso

### 1. Construir la imagen
Abre tu terminal en la raíz del repositorio y ejecuta:

```bash
docker build -t mi-web-estatica:v1.0 semana-00-fundamentos-docker/1.ejemplos/01-servidor-web-html
```

Verifica que la imagen se creó correctamente:
```bash
docker images | grep mi-web-estatica
```
> Observa el tamaño: ¡Apenas ocupa ~25MB gracias a Alpine Linux!

---

### 2. Ejecutar el contenedor
Corre el contenedor en segundo plano (`-d`) mapeando el puerto `8080` de tu máquina hacia el puerto `80` interno del contenedor:

```bash
docker run -d -p 8080:80 --name mi-servidor-web mi-web-estatica:v1.0
```

Verifica que esté activo:
```bash
docker ps
```

---

### 3. Probar la página web
* **En tu navegador:** Abre **[http://localhost:8080](http://localhost:8080)** para ver la página web servida con éxito por tu contenedor.
* **En tu terminal:**
  ```bash
  curl -I http://localhost:8080
  ```
  Verás las cabeceras HTTP de respuesta confirmando el servidor Nginx:
  ```http
  HTTP/1.1 200 OK
  Server: nginx/...
  Content-Type: text/html
  ```

---

### 4. Inspeccionar los logs en vivo
Cada vez que recargas la página en el navegador, Nginx genera un registro en la salida estándar (`stdout`):

```bash
docker logs -f mi-servidor-web
```
*(Presiona `Ctrl + C` para salir de los logs).*

---

### 5. Entrar al contenedor con `docker exec`
Explora el sistema de archivos del contenedor en ejecución:

```bash
docker exec -it mi-servidor-web sh
```
Dentro del contenedor ejecuta:
```sh
cat /usr/share/nginx/html/index.html
exit
```

---

### 6. Escaneo de Seguridad con Trivy (CLI)
Audita la imagen recién construida directamente desde tu línea de comandos con el paquete `trivy` para comprobar que la capa base de Alpine Nginx no contenga vulnerabilidades críticas:

```bash
# 1. Escanear la imagen construida (CLI como paquete):
trivy image --severity HIGH,CRITICAL mi-web-estatica:v1.0

# 2. Auditar buenas prácticas en el Dockerfile:
trivy config semana-00-fundamentos-docker/1.ejemplos/01-servidor-web-html

# Alternativa mediante contenedor efímero (si no tienes el paquete instalado):
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image --severity HIGH,CRITICAL mi-web-estatica:v1.0
```

> 🛡️ **Resultado esperado:** Gracias a `nginx:alpine`, Trivy mostrará **0 vulnerabilidades de severidad ALTA o CRÍTICA**. Consulta la [Guía de Seguridad con Trivy](../../../recursos/guia-trivy-seguridad.md) para más opciones de filtrado.

---

### 7. Detener y limpiar
Cuando termines de practicar:

```bash
docker rm -f mi-servidor-web
```

---

## 🧠 Conceptos Clave Aprendidos

1. **`FROM`**: Define la capa base. Usar tags basados en `alpine` reduce drásticamente el peso de la imagen y la superficie de vulnerabilidades.
2. **`COPY`**: Transfiere archivos desde tu máquina física (contexto de build) hacia el sistema de archivos de la imagen.
3. **`EXPOSE`**: Documenta qué puerto espera tráfico la aplicación (no publica el puerto hacia afuera por sí solo; eso lo hace el flag `-p` de `docker run`).
4. **`CMD` en primer plano (`daemon off;`)**: Los contenedores viven mientras su proceso principal (PID 1) esté activo. Si Nginx corriera en segundo plano (*daemon*), el contenedor terminaría inmediatamente.
