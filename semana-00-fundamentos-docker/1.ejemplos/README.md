# 📂 Ejemplos Prácticos de Docker a Kubernetes (Semana 0)

En esta carpeta encontrarás ejemplos directos para aprender a empaquetar tus aplicaciones con Docker y transferirlas hacia un clúster de Kubernetes en **Kind**.

---

## 📑 Índice de Ejemplos

| Carpeta / Archivo | Tipo de Aplicación | Concepto Clave |
| :--- | :--- | :--- |
| [`01-servidor-web-html/`](./01-servidor-web-html) | Sitio Web Estático (Nginx) | `FROM`, `COPY`, `EXPOSE` y `CMD` básico con Nginx. |
| [`02-app-python-api/`](./02-app-python-api) | API REST en Python (Microservicio) | **Buenas prácticas:** Usuario no-root (`USER appuser`), `COPY --chown`, `WORKDIR`, `ENV`, `.dockerignore` y proceso PID 1. |
| [`03-k8s-pod/pod-app-python.yaml`](./03-k8s-pod/pod-app-python.yaml) | Manifiesto Pod de Kubernetes | Despliegue de imagen local con `imagePullPolicy: IfNotPresent` y validación de seguridad con `securityContext.runAsNonRoot: true`. |

---

## 🛡️ Buenas Prácticas Aplicadas en la API de Ejemplo

1. **Principio de Menor Privilegio (Least Privilege):** Por defecto, los contenedores de Docker corren como `root` (UID 0). Si un atacante compromete tu app, tendría control total de los procesos. En el `Dockerfile` creamos un usuario dedicado (`appuser` con UID 10001) y cambiamos a él con la directiva `USER appuser`.
2. **Propiedad de Archivos (`--chown`):** Copiamos el código directamente asignando propiedad a `appuser:appgroup` para evitar inconsistencias de permisos de lectura y ejecución.
3. **Imágenes base oficiales y ligeras:** Usamos `python:3.12-alpine` para mantener la imagen en ~50MB y reducir la superficie de ataque.
4. **Contexto limpio con `.dockerignore`:** Excluye archivos temporales de Python (`__pycache__`) y configuraciones locales.
5. **Forma `exec` en `CMD`:** Usar `CMD ["python", "app.py"]` (con corchetes) permite que Python reciba directamente las señales de parada del sistema operativo (`SIGTERM`) para apagarse limpiamente.

---

## 🚀 Flujo Completo: De Docker a Kubernetes

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

### 2. Probar la imagen localmente con Docker
Ejecuta el contenedor en segundo plano (`-d`) mapeando el puerto `8080`:

```bash
docker run -d -p 8080:8080 --name test-api-local mi-api-cnm:v1.0
```

* **Verifica que esté vivo:** `docker ps`
* **Prueba el endpoint en tu terminal:** `curl http://localhost:8080`
  * *Observa la respuesta:* Verás `"usuario_proceso": "appuser (UID: 10001)"` y `"es_root": false`. ¡El contenedor está protegido!
* **Prueba el endpoint de salud:** `curl http://localhost:8080/health`
* **Mira los logs que imprimió la app:** `docker logs -f test-api-local`

Una vez validado, detén y elimina el contenedor de prueba:
```bash
docker stop test-api-local && docker rm test-api-local
```

---

### 3. Cargar la imagen en tu clúster de Kind
Como la imagen `mi-api-cnm:v1.0` solo existe en tu computador y no en Docker Hub, debemos inyectarla a los nodos de Kind:

```bash
kind load docker-image mi-api-cnm:v1.0 --name cnm-lab
```
*(Si tu clúster tiene otro nombre, cambia `--name <nombre-cluster>`)*.

---

### 4. Desplegar la imagen en Kubernetes con seguridad activa
Aplica el manifiesto YAML que incluye `securityContext`:

```bash
kubectl apply -f semana-00-fundamentos-docker/1.ejemplos/03-k8s-pod/pod-app-python.yaml
```

Verifica el estado del Pod:
```bash
kubectl get pods
```

Deberás ver `api-python-desde-docker` en estado `Running`. Como la imagen fue construida con `USER appuser`, cumple exitosamente con la regla `runAsNonRoot: true` exigida por Kubernetes.

---

### 5. Abrir túnel con `port-forward`
Conéctate desde tu navegador abriendo un túnel directo al Pod:

```bash
kubectl port-forward pod/api-python-desde-docker 8080:8080
```

Visita **[http://localhost:8080](http://localhost:8080)** y verás que ahora el `hostname_o_pod` corresponde exactamente al nombre del Pod asignado por Kubernetes.

