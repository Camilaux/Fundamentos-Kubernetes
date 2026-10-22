# 🎯 Reto 3: El contenedor vulnerable que corre como root

* **Dificultad:** 🟡 Intermedio
* **Archivos:** [`Dockerfile`](./Dockerfile) y [`pod-seguro.yaml`](./pod-seguro.yaml)

---

## 🔍 El Escenario

Tu equipo implementó políticas de seguridad en el clúster de Kubernetes usando `securityContext.runAsNonRoot: true`. Un compañero empaquetó una API con Docker, pero al desplegarla en Kubernetes, el Pod entra en error de inmediato.

### 💥 Síntomas

1. **En Docker local:**
   ```bash
   docker build -t reto-root:v1.0 semana-00-fundamentos-docker/2.reto-roto/03-contenedor-como-root
   docker run --rm reto-root:v1.0 whoami
   ```
   *Salida:* `root` ❌ (El proceso corre con los máximos privilegios de superusuario).

2. **En Kubernetes:**
   ```bash
   kind load docker-image reto-root:v1.0 --name cnm-lab
   kubectl apply -f semana-00-fundamentos-docker/2.reto-roto/03-contenedor-como-root/pod-seguro.yaml
   kubectl get pods
   ```
   *Salida:*
   ```text
   NAME               READY   STATUS                       RESTARTS   AGE
   reto-root-en-k8s   0/1     CreateContainerConfigError   0          10s
   ```
   Al revisar los eventos con `kubectl describe pod reto-root-en-k8s`:
   `Error: container has runAsNonRoot and image will run as root`

---

## 🎯 Tu Misión

1. Modifica [`Dockerfile`](./Dockerfile) para:
   * Crear un usuario y grupo no-root en Alpine (por ejemplo `appuser` con UID `10001`).
   * Asignar la propiedad de los archivos copiados con `--chown=appuser:appgroup`.
   * Declarar la instrucción `USER appuser` antes de `CMD`.
2. Vuelve a compilar la imagen:
   ```bash
   docker build -t reto-root:v1.0 semana-00-fundamentos-docker/2.reto-roto/03-contenedor-como-root
   ```
3. Valida en Docker que `docker run --rm reto-root:v1.0 whoami` responda `appuser`.
4. Vuelve a cargar la imagen en Kind:
   ```bash
   kind load docker-image reto-root:v1.0 --name cnm-lab
   ```
5. Elimina y vuelve a aplicar el Pod (`kubectl delete -f ...` y `kubectl apply -f ...`). ¡Ahora debe pasar a estado `Running`! 🚀
