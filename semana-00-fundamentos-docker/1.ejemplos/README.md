# 📂 Ejemplos Prácticos de Docker (Semana 0)

En esta carpeta encontrarás ejemplos directos para aprender a empaquetar tus aplicaciones con Docker aplicando las mejores prácticas de la industria.

---

## 📑 Índice de Ejemplos

| Carpeta | Tipo de Aplicación | Concepto Clave |
| :--- | :--- | :--- |
| [`01-servidor-web-html/`](./01-servidor-web-html) | Sitio Web Estático (Nginx) | `FROM`, `COPY`, `EXPOSE` y `CMD` básico con Nginx en primer plano. |
| [`02-app-python-api/`](./02-app-python-api) | API REST en Python (Microservicio) | **Buenas prácticas:** Usuario no-root (`USER appuser`), `COPY --chown`, `WORKDIR`, `ENV`, `.dockerignore` y proceso PID 1. |

---

## 🛡️ Buenas Prácticas Aplicadas en la API de Ejemplo

1. **Principio de Menor Privilegio (Least Privilege):** Por defecto, los contenedores de Docker corren como `root` (UID 0). Si un atacante compromete tu app, tendría control total de los procesos. En el `Dockerfile` creamos un usuario dedicado (`appuser` con UID 10001) y cambiamos a él con la directiva `USER appuser`.
2. **Propiedad de Archivos (`--chown`):** Copiamos el código directamente asignando propiedad a `appuser:appgroup` para evitar inconsistencias de permisos de lectura y ejecución.
3. **Imágenes base oficiales y ligeras:** Usamos `python:3.12-alpine` para mantener la imagen en ~50MB y reducir la superficie de ataque.
4. **Contexto limpio con `.dockerignore`:** Excluye archivos temporales de Python (`__pycache__`) y configuraciones locales.
5. **Forma `exec` en `CMD`:** Usar `CMD ["python", "app.py"]` (con corchetes) permite que Python reciba directamente las señales de parada del sistema operativo (`SIGTERM`) para apagarse limpiamente.

---

## 🚀 Flujo Práctico Paso a Paso con Docker

### 1. Construir la imagen de la API en Python
Abre tu terminal en la raíz del repositorio y ejecuta:

```bash
docker build -t mi-api-cnm:v1.0 semana-00-fundamentos-docker/1.ejemplos/02-app-python-api
```

Verifica que tu imagen fue creada con éxito:
```bash
docker images | grep mi-api-cnm
```

---

### 2. Ejecutar el contenedor en segundo plano
Corre el contenedor mapeando el puerto `8080`:

```bash
docker run -d -p 8080:8080 --name test-api-local mi-api-cnm:v1.0
```

* **Verifica que esté vivo:** `docker ps`
* **Prueba el endpoint en tu navegador:** Abre **[http://localhost:8080](http://localhost:8080)** para disfrutar la **interfaz web interactiva**: verás la taza de tinto paisa humeando con vapor animado, sonido de servicio con Web Audio API y simulador de variables de entorno en vivo.
* **Prueba el endpoint en tu terminal:** `curl http://localhost:8080`
  * *Observa la respuesta JSON:* Verás `"usuario_proceso": "appuser (UID: 10001)"` y `"es_root": false`. ¡El contenedor está protegido!
* **Prueba el endpoint de salud:** `curl http://localhost:8080/health`
* **Mira los logs en vivo:** `docker logs -f test-api-local`

---

### 3. Probar sobrescritura de variables de entorno con `-e`
Puedes cambiar el comportamiento de la aplicación en tiempo de ejecución sin reconstruir la imagen:

```bash
docker run -d -p 8081:8080 -e MENSAJE="¡Saludos desde el Poblado en Medellín! ☕" --name test-api-env mi-api-cnm:v1.0
curl http://localhost:8081
```

---

### 4. Entrar a inspeccionar el contenedor con `docker exec`
Abre una terminal interactiva dentro del contenedor activo:

```bash
docker exec -it test-api-local sh
```
Dentro del contenedor prueba ejecutar:
```sh
whoami    # Responderá: appuser
id        # UID 10001(appuser) GID 10001(appgroup)
exit
```

---

### 5. Detener y limpiar los contenedores de prueba
Cuando termines de practicar:

```bash
docker rm -f test-api-local test-api-env
```

> [!TIP]
> 👉 **¿Cuándo entra Kubernetes?**  
> En la **Semana 1** aprenderás a instalar tu clúster local con Kind y a orquestar contenedores usando Pods, Services y Deployments.


