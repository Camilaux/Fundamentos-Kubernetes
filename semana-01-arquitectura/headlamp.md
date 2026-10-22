# 🖥️ Consola Visual Open Source: Headlamp

**[Headlamp](https://headlamp.dev/)** es una consola web y de escritorio moderna, extensible y de código abierto para Kubernetes, respaldada oficialmente por **Kubernetes SIGs**.

Te permite inspeccionar el clúster, ver los nodos, namespaces, pods, contenedores, logs en tiempo real, eventos y métricas de forma visual, lo que facilita entender mucho más rápido la arquitectura y diagnosticar problemas sin depender exclusivamente de comandos en la terminal.

* 🌐 **Sitio oficial:** [https://headlamp.dev/](https://headlamp.dev/)
* 📚 **Documentación oficial:** [https://headlamp.dev/docs/latest/](https://headlamp.dev/docs/latest/)
* 📦 **Repositorio oficial de Helm:** [https://kubernetes-sigs.github.io/headlamp/](https://kubernetes-sigs.github.io/headlamp/)
* 🐙 **Releases oficiales en GitHub:** [https://github.com/kubernetes-sigs/headlamp/releases](https://github.com/kubernetes-sigs/headlamp/releases)

---

## 📑 Elige cómo quieres usar Headlamp

| Modalidad | Ideal si... | Requisitos |
| :--- | :--- | :--- |
| **[Opción 1: App de Escritorio](#-opción-1-como-aplicación-de-escritorio-desktop-app)** | Quieres la experiencia más rápida y ligera sin tocar el clúster. | macOS, Windows o Linux. |
| **[Opción 2: Dentro del Clúster](#️-opción-2-despliegue-dentro-del-clúster-con-helm-y-nodeport)** | Quieres que la consola viva como un servicio en Kubernetes accesible por red. | Clúster activo y Helm instalado. |
| **[Opción 3: Contenedor Docker](#-opción-3-ejecutar-como-contenedor-de-docker-local)** | Prefieres no instalar apps de escritorio ni instalar nada dentro del clúster. | Docker Desktop / Docker Engine. |

---

## 💻 Opción 1: Como Aplicación de Escritorio (Desktop App)

Esta es la forma **más sencilla y recomendada** para principiantes: instalas la aplicación directamente en tu sistema operativo y ella detecta automáticamente tus clústeres leyendo tu archivo local `~/.kube/config` (el mismo que usa `kubectl`).

* 📖 **Documentación oficial de Desktop:** [https://headlamp.dev/docs/latest/installation/desktop/](https://headlamp.dev/docs/latest/installation/desktop/)

### Instalación por sistema operativo:

#### 🍏 macOS
Instálalo con Homebrew Cask o descargando el archivo `.dmg` desde [GitHub Releases](https://github.com/kubernetes-sigs/headlamp/releases):
```bash
brew install --cask headlamp
```

#### 🪟 Windows
Instálalo con Winget, Chocolatey o descargando el archivo `.exe` desde [GitHub Releases](https://github.com/kubernetes-sigs/headlamp/releases):
```powershell
# Con Windows Package Manager (Winget):
winget install Headlamp.Headlamp

# O con Chocolatey:
choco install headlamp
```

#### 🐧 Linux
Disponible como Flatpak, AppImage o instaladores `.deb` y `.rpm`:
```bash
# Con Flatpak:
flatpak install flathub io.headlamp.Headlamp
flatpak run io.headlamp.Headlamp
```
*(O descarga el archivo `.AppImage` o paquete `.deb`/`.rpm` directamente desde [GitHub Releases](https://github.com/kubernetes-sigs/headlamp/releases)).*

---

## 🛠️ Opción 2: Despliegue dentro del Clúster (con Helm y NodePort)

Esta opción instala la interfaz web de Headlamp como un servicio dentro de tu clúster de Kubernetes, exponiéndolo a través de un puerto de tipo `NodePort`.

### 📦 Prerrequisito: Instalar Helm
Headlamp se despliega mediante [**Helm**](https://helm.sh/) (el gestor de paquetes estándar de Kubernetes). Si aún no lo tienes instalado:

* **macOS (Homebrew):** `brew install helm`
* **Linux:** `curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash`
* **Windows (PowerShell):** `winget install Helm.Helm` o `choco install kubernetes-helm`
* 👉 *Guía oficial:* [helm.sh/docs/intro/install/](https://helm.sh/docs/intro/install/)

---

### 🚀 Paso a Paso de Instalación

#### 1. Añadir y actualizar el repositorio de Helm
```bash
helm repo add headlamp https://kubernetes-sigs.github.io/headlamp/
helm repo update
```

#### 2. Instalar Headlamp en `kube-system` como `NodePort`
```bash
helm install headlamp headlamp/headlamp --namespace kube-system --set service.type=NodePort
```

> [!NOTE]
> **¿Qué hace `--set service.type=NodePort`?**  
> Por defecto, los servicios en Kubernetes se crean como `ClusterIP` (accesibles solo internamente). Al definir `service.type=NodePort`, Kubernetes reserva un puerto de alto rango (entre `30000` y `32767`) en cada nodo del clúster para que podamos acceder a la consola desde el navegador.

#### 3. Crear el Secret con el Token de Administrador
Headlamp necesita un token con permisos para leer los recursos del clúster. El chart de Helm crea automáticamente el `ServiceAccount` llamado `headlamp` en `kube-system`; creamos un `Secret` asociado a él para generar el token:

```bash
kubectl apply -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: headlamp-admin
  namespace: kube-system
  annotations:
    kubernetes.io/service-account.name: headlamp
type: kubernetes.io/service-account-token
EOF
```

> [!IMPORTANT]
> **¿Por qué creamos este Secret manualmente?**  
> Desde Kubernetes 1.24+, los `ServiceAccounts` no generan tokens permanentes en un Secret estático de forma automática por seguridad. La anotación `kubernetes.io/service-account.name: headlamp` le ordena al Control Plane generar y almacenar un token JWT persistente vinculado al usuario de servicio de Headlamp.

#### 4. Validar el puerto asignado al NodePort y la IP del Nodo
Para conectarte a través de NodePort necesitas dos datos: el **puerto** y la **IP del nodo**.

1. **Obtener el puerto NodePort:**
   ```bash
   kubectl get svc -n kube-system | grep headlamp
   ```
   Verás una salida similar a:
   ```text
   headlamp   NodePort   10.96.120.45   <none>   80:31234/TCP   1m
   ```
   El número a la derecha de `80:` (en este ejemplo `31234`) es tu puerto `NodePort`.

2. **Obtener la IP del nodo (si usas Kind):**
   Dado que Kind ejecuta cada nodo dentro de un contenedor de Docker, puedes averiguar la IP interna del nodo con:
   ```bash
   kubectl get nodes -o wide
   ```
   Mira la columna `INTERNAL-IP` (por ejemplo: `172.18.0.2`).
   
   *(También puedes consultarla directamente con Docker: `docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' cnm-lab-control-plane`)*

#### 5. Obtener y decodificar el token de acceso
Kubernetes guarda los secretos en Base64. Extráelo y decodifícalo en tu terminal:
```bash
kubectl get secret headlamp-admin -n kube-system -o jsonpath='{.data.token}' | base64 --decode
```

> [!TIP]
> Copia la cadena generada (es un token JWT largo). Lo usarás en la pantalla de bienvenida de Headlamp para iniciar sesión.

#### 6. Conectarte a Headlamp

* **Opción A (Acceso directo por NodePort con la IP del nodo):**  
  Abre en tu navegador:
  ```text
  http://<IP_DEL_NODO>:<PUERTO_NODEPORT>
  ```
  *(Por ejemplo: `http://172.18.0.2:31234`)*
  
  > [!NOTE]
  > **¿Estás en Linux o en macOS/Windows?**  
  > * En **Linux**: La red de Docker es nativa y puedes acceder a `http://172.18.0.2:31234` directamente desde tu navegador.  
  > * En **macOS / Windows**: Docker Desktop corre dentro de una máquina virtual ligera, por lo que la IP interna `172.18.x.x` no es accesible directamente desde el navegador de tu máquina anfitriona sin configuración de enrutamiento previa. En estos sistemas operativos, la **Opción B** es la solución directa y recomendada.

* **Opción B (Acceso universal por túnel port-forward — recomendado):**  
  Funciona idéntico en cualquier sistema operativo sin importar la configuración de red:
  ```bash
  kubectl port-forward -n kube-system svc/headlamp 8000:80
  ```
  Abre en tu navegador **[http://localhost:8000](http://localhost:8000)**.

Pega el token generado en el paso 5 y haz clic en **Sign In**.

---

## 🐳 Opción 3: Ejecutar como Contenedor de Docker Local

Si tienes Docker instalado y prefieres no instalar aplicaciones en tu sistema ni desplegar charts en tu clúster, puedes levantar Headlamp en un contenedor independiente montando tu archivo local `~/.kube/config`:

* 📖 **Documentación oficial Docker:** [https://headlamp.dev/docs/latest/installation/#docker](https://headlamp.dev/docs/latest/installation/#docker)

### Ejecutar el contenedor:

* **En macOS y Linux:**
  ```bash
  docker run -d --name headlamp \
    -p 8080:80 \
    -v "$HOME/.kube/config:/.kube/config:ro" \
    ghcr.io/headlamp-k8s/headlamp:latest
  ```

* **En Windows (PowerShell):**
  ```powershell
  docker run -d --name headlamp `
    -p 8080:80 `
    -v "$env:USERPROFILE\.kube\config:/.kube/config:ro" `
    ghcr.io/headlamp-k8s/headlamp:latest
  ```

### Acceder y autenticarte:
1. Abre tu navegador en **[http://localhost:8080](http://localhost:8080)**.
2. Inicia sesión cargando tu archivo de configuración o utilizando el token de administrador generado en la Opción 2.

---

## ⬅️ Volver
* 🏠 [Volver al README de la Semana 1](./README.md)
* 🛠️ [Volver a Prepara tu Laboratorio](./0.prepara-tu-laboratorio/README.md)
