# 💥 Retos Rotos de la Semana 0: Docker y su Puente a Kubernetes

¡Bienvenido al laboratorio de investigación de fallos! Aquí aprenderás a depurar los **dos errores más frustrantes** que todo principiante sufre al empezar con Docker y Kubernetes.

---

## 🎯 Reto 1: El contenedor que se apaga solo al instante (PID 1)
* **Ubicación:** [`01-dockerfile-roto/Dockerfile`](./01-dockerfile-roto/Dockerfile)
* **Nivel:** 🟢 Principiante
* **Síntoma:** Construyes la imagen con éxito (`docker build`), pero al correrla en segundo plano con `docker run -d`, el contenedor se apaga de inmediato y desaparece de `docker ps`.
* **Herramientas de investigación:**
  * `docker ps -a` (para ver el código de salida).
  * `docker logs <id-contenedor>`
* **Misión:** Modifica la instrucción `CMD` del `Dockerfile` para que el servidor Nginx corra en primer plano (*foreground*).

---

## 🎯 Reto 2: El Pod que busca una imagen local fantasma
* **Ubicación:** [`02-pod-sin-cargar-a-kind.yaml`](./02-pod-sin-cargar-a-kind.yaml)
* **Nivel:** 🟡 Intermedio
* **Síntoma:** Construiste la imagen `mi-api-cnm:v1.0` en tu máquina, pero al aplicar el Pod en Kubernetes, se queda trabado en `ImagePullBackOff` o `ErrImagePull`.
* **Herramientas de investigación:**
  * `kubectl get pods`
  * `kubectl describe pod reto-docker-k8s` (lee los `Events` al final).
* **Misión:** 
  1. Carga la imagen al clúster de Kind con el comando correcto.
  2. Ajusta el parámetro `imagePullPolicy` en el manifiesto YAML para que use la copia local.

---

## 🏆 ¿Cómo enviar tu solución?
1. Corrige los archivos en tu máquina.
2. Cópialos a `aportes-comunidad/soluciones-retos/tu-usuario/semana-00/` con un comentario explicando qué causaba la falla.
3. Envía tu **Pull Request** siguiendo la guía de [`CONTRIBUTING.md`](../../CONTRIBUTING.md) para subir de rango en [`ASISTENTES.md`](../../ASISTENTES.md).
