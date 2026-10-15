# 🌱 Semana 1: El motor por dentro y tu primer Pod

¡Bienvenido a la primera semana! Hoy pasaremos de entender qué hace Kubernetes en teoría a levantar nuestro propio clúster local y desplegar nuestra primera aplicación.

---

## 🧠 Resumen en 2 minutos (Sin enredos)

Imagina que tienes una cafetería muy exitosa en Medellín:
* **El Contenedor (Docker):** Es la cafetera expreso empacada y lista para funcionar.
* **El Pod:** Es la **estación de café** donde conectas esa cafetera (le da electricidad, agua y un lugar físico). En Kubernetes nunca pones cafeteras sueltas en el piso; siempre van dentro de un **Pod**.
* **El Worker Node (Nodo trabajador):** Es el local físico donde caben varias estaciones de café.
* **El Control Plane (Cerebro):** Es el administrador del negocio que vigila que todas las estaciones estén funcionando.

```mermaid
graph TD
    U["👨‍💻 Tú (kubectl)"] -->|"1. Quiero un Pod con Nginx"| API["🧠 Control Plane (API Server)"]
    API -->|"2. Asigna un servidor libre"| N1["💪 Worker Node"]
    subgraph N1 ["💪 Worker Node (Tu Computador)"]
        K["👷 Kubelet (Capataz)"] -->|"3. Crea la cápsula"| P["📦 Pod (IP: 10.244.0.5)"]
        subgraph P ["📦 Pod"]
            C["🐳 Contenedor Nginx (Puerto 80)"]
        end
    end
```

---

## 🧪 Laboratorio en Vivo (Hands-on)

### Paso 1: Crea tu clúster local
Si usas **Kind**, abre tu terminal y ejecuta:
```bash
kind create cluster --name cnm-lab
```
Verifica que tu clúster esté vivo:
```bash
kubectl cluster-info
kubectl get nodes
```

### Paso 2: Despliega tu primer Pod
Explora la carpeta [`1.ejemplos`](./1.ejemplos) y aplica el primer Pod básico en tu clúster:
```bash
kubectl apply -f semana-01-arquitectura/1.ejemplos/01-mi-primer-pod.yaml
```
*(También puedes probar un Pod multi-contenedor con dos contenedores usando `02-pod-multi-contenedor.yaml`)*


Revisa que esté corriendo (`Running`):
```bash
kubectl get pods
```

### Paso 3: Conéctate a tu Pod desde tu navegador
Usa `port-forward` para abrir un túnel desde tu computador hasta el Pod:
```bash
kubectl port-forward pod/hola-medellin 8080:80
```
👉 Abre en tu navegador **[http://localhost:8080](http://localhost:8080)** y verás tu servidor respondiendo.

---

## 💥 El Reto Roto de la Semana 1

Entra a la carpeta [`reto-roto/pod-con-errores.yaml`](./reto-roto/pod-con-errores.yaml). Un compañero intentó desplegar un Pod pero cometió **2 errores muy comunes** y el Pod nunca pasa a estado `Running`.

### ¿Cómo superarlo?
1. Intenta aplicarlo en tu clúster: `kubectl apply -f semana-01-arquitectura/reto-roto/pod-con-errores.yaml`
2. Investiga qué le duele usando:
   * `kubectl get pods`
   * `kubectl describe pod pod-rebelde`
3. Copia el archivo a `aportes-comunidad/soluciones-retos/tu-usuario/semana-01/pod-solucionado.yaml`, corrígelo, agrega un comentario `#` explicando qué estaba mal y envía tu **Pull Request**.


## 🕵️‍♂️ Diccionario Rápido: ¿Qué le duele a mi Pod?

Cuando ejecutes `kubectl get pods`, el estado (`STATUS`) te dará la primera pista de dónde buscar:

| Estado del Pod | ¿Qué significa en español? | Comando para descubrir el culpable |
| :--- | :--- | :--- |
| **`Pending`** | El Pod está en la sala de espera. Ningún servidor tiene suficiente RAM/CPU libre para recibirlo. | `kubectl describe pod <nombre>` *(Mira la tabla de Events al final)*. |
| **`ImagePullBackOff`** o **`ErrImagePull`** | Kubernetes intentó descargar la imagen de Docker pero no existe, está mal escrita o es privada. | `kubectl describe pod <nombre>` *(Revisa qué imagen intentó bajar)*. |
| **`CrashLoopBackOff`** | El contenedor logró arrancar, pero la aplicación de adentro falló y se apagó sola. | `kubectl logs <nombre>` *(Lee el error que arrojó la aplicación)*. |
| **`Error de validación al hacer apply`** | El archivo YAML tiene un error de sintaxis, indentación o un nombre de campo inventado. | Lee el número de línea que te muestra la terminal al hacer `kubectl apply`. |