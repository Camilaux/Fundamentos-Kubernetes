# 🎯 Reto 2: El Pod que busca una imagen fantasma en internet

* **Dificultad:** 🟡 Intermedio
* **Archivo:** [`pod-roto.yaml`](./pod-roto.yaml)

---

## 🔍 El Escenario

Construiste exitosamente tu imagen `mi-api-cnm:v1.0` en tu computador usando `docker build`. Todo funcionó perfecto en Docker local.

Sin embargo, cuando intentas desplegarla en tu clúster de Kubernetes aplicando el manifiesto:
```bash
kubectl apply -f semana-00-fundamentos-docker/2.reto-roto/02-pod-sin-cargar-a-kind/pod-roto.yaml
```

Al revisar el estado con `kubectl get pods`:
```text
NAME              READY   STATUS             RESTARTS   AGE
reto-docker-k8s   0/1     ImagePullBackOff   0          30s
```

¡El Pod se queda eternamente en `ImagePullBackOff` o `ErrImagePull` y nunca pasa a `Running`!

---

## 🕵️‍♂️ Herramientas de Investigación

1. Ejecuta:
   ```bash
   kubectl describe pod reto-docker-k8s
   ```
2. Desplázate hasta la sección **Events** al final de la salida.
3. Observa qué intentó hacer Kubernetes:  
   `Failed to pull image "mi-api-cnm:v1.0": rpc error: ... not found`

---

## 💡 ¿Por qué ocurre esto? (Las 2 causas)

1. **Kind corre dentro de contenedores de Docker:** Tu clúster local de Kind no tiene acceso automático a las imágenes de tu Docker local hasta que se las inyectas explícitamente.
2. **La trampa de `imagePullPolicy: Always`:** Si el manifiesto YAML tiene `imagePullPolicy: Always`, Kubernetes ignora cualquier imagen que exista localmente en los nodos y fuerza una descarga desde Docker Hub (donde tu imagen privada no existe).

---

## 🎯 Tu Misión

1. Carga la imagen local de tu Docker hacia los nodos de Kind:
   ```bash
   kind load docker-image mi-api-cnm:v1.0 --name cnm-lab
   ```
   *(Si tu clúster tiene otro nombre, reemplaza `cnm-lab`)*.

2. Abre [`pod-roto.yaml`](./pod-roto.yaml) y cambia:
   ```yaml
   imagePullPolicy: Always
   ```
   por:
   ```yaml
   imagePullPolicy: IfNotPresent
   ```

3. Vuelve a aplicar el Pod:
   ```bash
   kubectl apply -f semana-00-fundamentos-docker/2.reto-roto/02-pod-sin-cargar-a-kind/pod-roto.yaml
   ```

4. Valida con `kubectl get pods` que pase a estado `Running` ✅.
