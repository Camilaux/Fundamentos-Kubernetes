> [!TIP]
> **¿No puedes instalar Docker o Kind en tu computador?**  
> Si tu equipo tiene recursos limitados de RAM/CPU o restricciones en tu sistema operativo, puedes practicar de forma 100% gratuita y en el navegador con terminales interactivas en la nube:
> * 🐳 **Laboratorios de Docker:** [KodeKloud Studio — Docker Labs](https://kodekloud.com/studio/labs/docker)
> * ☸️ **Laboratorios de Kubernetes:** [KodeKloud Studio — Kubernetes Labs](https://kodekloud.com/studio/labs/kubernetes)

## 🐳 ¿Qué es Kind y por qué lo usamos en el Workshop?

**Kind** significa **K**ubernetes **in** **D**ocker. 

Tradicionalmente, para tener un clúster de Kubernetes en tu computador necesitabas crear varias máquinas virtuales pesadas que consumían toda tu memoria RAM. **Kind hace trampa (de la buena):** simula cada servidor de Kubernetes (*Nodo*) usando un simple contenedor de Docker. Es súper rápido, ligero y se borra en segundos sin dejar basura en tu sistema.

### ⚡ Comandos básicos de Kind que usarás todos los días

```bash
# 1. Crear un clúster sencillo (1 solo nodo) con nombre personalizado
kind create cluster --name cnm-lab

# 2. Ver cuántos clústeres de Kind tienes creados
kind get clusters

# 3. Crear un clúster personalizado usando un archivo YAML (¡Lo haremos abajo!)
kind create cluster --name cnm-pro --config semana-01-arquitectura/0.prepara-tu-laboratorio/kind-multinode.yaml

# 4. Borrar un clúster cuando termines de practicar (libera tu RAM)
kind delete cluster --name cnm-lab
```

---

## 🛠️ Personalizando tu Clúster de Kind con YAML

Por defecto, Kind crea un solo servidor que hace de jefe (*Control Plane*) y obrero (*Worker*) al mismo tiempo. En esta carpeta tienes plantillas YAML para crear clústeres como en el mundo real:

<details>
<summary><b>📄 1. Clúster Multi-Nodo Estándar (1 Cerebro + 2 Obreros) — <code>kind-multinode.yaml</code></b></summary>
<br>

Ideal para ver cómo Kubernetes reparte tus Pods en distintos servidores usando el CNI estándar de Kind (`kindnet`). Funciona directamente de la caja sin pasos adicionales:

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  # El cerebro del clúster (Control Plane)
  - role: control-plane
  # Los servidores obreros donde correrán tus aplicaciones
  - role: worker
  - role: worker
```

**Cómo crearlo:**
```bash
kind create cluster --name cnm-multinodo --config semana-01-arquitectura/0.prepara-tu-laboratorio/kind-multinode.yaml
```
*En unos segundos todos tus nodos estarán automáticamente en estado `Ready`.*
</details>

<details>
<summary><b>🐝 2. Clúster Multi-Nodo con Cilium CNI (1 Cerebro + 2 Obreros) — <code>kind-cilium.yaml</code></b></summary>
<br>

**Cilium** es un plugin de red (CNI) de última generación impulsado por **eBPF** (tecnología que inyecta programas seguros directamente en el kernel de Linux sin tocar el código fuente). Proporciona conectividad de red de altísimo rendimiento, seguridad avanzada y observabilidad profunda para tus Pods.

### Manifiesto de Kind (`kind-cilium.yaml`):

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4

# Deshabilitamos el CNI por defecto (kindnet) para que Cilium tome el control
networking:
  disableDefaultCNI: true
  # Opcional: Reemplazo completo de kube-proxy mediante eBPF
  # kubeProxyMode: "none"

nodes:
  # El cerebro del clúster (Control Plane)
  - role: control-plane
  # Servidores obreros donde correrán los Pods y el agente de Cilium
  - role: worker
  - role: worker
```

### Paso a paso para crearlo e instalar Cilium:

#### 1. Crear el clúster con Kind:
```bash
kind create cluster --name cnm-cilium --config semana-01-arquitectura/0.prepara-tu-laboratorio/kind-cilium.yaml
```

> [!NOTE]
> **¿Por qué los nodos arrancan en estado `NotReady`?**  
> Al desactivar el CNI por defecto (`disableDefaultCNI: true`), los nodos no tienen un proveedor de red asignado aún. Es completamente normal que `kubectl get nodes` muestre `NotReady` hasta que Cilium quede instalado y asigne las redes a cada nodo.

#### 2. Instalar el CLI de Cilium (o usar Helm):

* **En macOS (Homebrew):**
  ```bash
  brew install cilium-cli
  ```
* **En Linux:**
  ```bash
  CILIUM_CLI_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/cilium-cli/main/stable.txt)
  CLI_ARCH=amd64
  if [ "$(uname -m)" = "arm64" ]; then CLI_ARCH=arm64; fi
  curl -L --fail --remote-name-all https://github.com/cilium/cilium-cli/releases/download/${CILIUM_CLI_VERSION}/cilium-linux-${CLI_ARCH}.tar.gz
  sudo tar xzvfC cilium-linux-${CLI_ARCH}.tar.gz /usr/local/bin
  rm cilium-linux-${CLI_ARCH}.tar.gz
  ```
* *(Alternativa con Helm si no usas cilium-cli):*
  ```bash
  helm repo add cilium https://helm.cilium.io/
  helm repo update
  helm install cilium cilium/cilium --namespace kube-system
  ```

#### 3. Desplegar Cilium en el clúster:
```bash
cilium install
```

#### 4. Validar que todo esté verde (`Ready`):
```bash
# Espera a que los pods de Cilium estén listos
cilium status --wait

# Revisa tus nodos: ¡ahora todos deben estar en Ready!
kubectl get nodes
```

> [!TIP]
> Puedes validar la conectividad interna completa entre Pods ejecutando:
> ```bash
> cilium connectivity test
> ```

</details>

<details>
<summary><b>🌐 3. Clúster listo para Ingress (Puertos 80 y 443 abiertos) — <code>kind-ingress.yaml</code></b></summary>
<br>

Ideal para la **Semana 3 (Redes)**. Conecta los puertos `80` y `443` de tu computador directamente con el clúster para abrir tus aplicaciones en el navegador sin usar `port-forward`:

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
    kubeadmConfigPatches:
      - |
        kind: InitConfiguration
        nodeRegistration:
          kubeletExtraArgs:
            node-labels: "ingress-ready=true"
    extraPortMappings:
      - containerPort: 80
        hostPort: 80
        protocol: TCP
      - containerPort: 443
        hostPort: 443
        protocol: TCP
  - role: worker
```
**Cómo crearlo:**
```bash
kind create cluster --name cnm-redes --config semana-01-arquitectura/0.prepara-tu-laboratorio/kind-ingress.yaml
```
</details>

---

## 🧰 Kit de Supervivencia: Si tienes varios clústeres

Cuando tienes el clúster del trabajo, el de pruebas y el del workshop al mismo tiempo, es muy fácil equivocarse y lanzar un comando donde no debes. Estas **herramientas gratuitas** te harán la vida mucho más fácil:

| Herramienta | ¿Para qué sirve en palabras sencillas? | Cómo se usa |
| :--- | :--- | :--- |
| **[Headlamp](https://headlamp.dev/)** | **La consola web visual.** Panel de control open source en el navegador para inspeccionar Pods, Nodos, logs y eventos sin memorizar comandos. | Despliégalo con Helm y accede en `http://localhost:8000` *(guía detallada abajo)*. |
| **[kubectx](https://github.com/ahmetb/kubectx)** | **El control remoto de clústeres.** Te permite saltar de un clúster a otro en 1 segundo sin comandos largos. | `kubectx` *(lista tus clústeres)*<br>`kubectx kind-cnm-lab` *(cambia de clúster)*<br>`kubectx -` *(vuelve al clúster anterior)* |
| **[kubens](https://github.com/ahmetb/kubectx)** | **El selector de carpetas (Namespaces).** Se instala junto con `kubectx` y te ahorra escribir `-n mi-namespace` en cada comando. | `kubens` *(lista los namespaces)*<br>`kubens kube-system` *(entra a ese namespace)* |
| **[k9s](https://k9scli.io/)** | **El panel de control en tu terminal.** Es una interfaz visual interactiva dentro de la consola para ver logs, entrar a Pods y borrar recursos con atajos de teclado. | Solo escribe `k9s` en tu terminal y muévete con las flechas. |
| **[stern](https://github.com/stern/stern)** | **El megáfono de logs.** Te permite ver los logs de muchos Pods al mismo tiempo y con colores distintos. | `stern mi-app` *(muestra los logs en vivo de todas las réplicas de tu app)*. |

> [!TIP]
> **El truco de velocidad número 1:** Agrega un alias en tu terminal para no escribir `kubectl` completo mil veces.
> Ejecuta `alias k=kubectl` y ahora podrás escribir simplemente `k get pods` o `k describe pod mi-pod`.

---

## 🖥️ Consola Visual Open Source: Headlamp

Para gestionar tu clúster de forma gráfica e intuitiva y entender la relación entre nodos, pods y namespaces mucho más rápido, puedes usar **[Headlamp](https://headlamp.dev/)**, una consola web y de escritorio open source respaldada por Kubernetes SIGs.

> 📖 **Guía completa y detallada:** Puedes consultar la guía completa con explicaciones paso a paso en [**`semana-01-arquitectura/headlamp.md`**](../headlamp.md).

### 🚀 Despliegue en el Clúster con Helm (como NodePort)

1. **Añadir repositorio de Helm:**
   ```bash
   helm repo add headlamp https://kubernetes-sigs.github.io/headlamp/
   helm repo update
   ```

2. **Instalar Headlamp como NodePort en `kube-system`:**
   ```bash
   helm install headlamp headlamp/headlamp --namespace kube-system --set service.type=NodePort
   ```

3. **Crear el Secret para obtener el Token de Administrador:**
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

4. **Validar el puerto NodePort y la IP del nodo:**
   ```bash
   # Ver el puerto asignado (ej. 80:31234/TCP)
   kubectl get svc -n kube-system | grep headlamp

   # Si usas Kind, ver la IP interna del nodo (columna INTERNAL-IP, ej. 172.18.0.2)
   kubectl get nodes -o wide
   ```

5. **Obtener y decodificar el token de acceso:**
   ```bash
   kubectl get secret headlamp-admin -n kube-system -o jsonpath='{.data.token}' | base64 --decode
   ```

6. **Acceder a la consola:**
   * **Por NodePort con la IP del nodo (Linux):** Abre `http://<IP_DEL_NODO>:<PUERTO_NODEPORT>` (ej. `http://172.18.0.2:31234`).
   * **Por Port-Forward (Universal en Windows/macOS/Linux):**
     ```bash
     kubectl port-forward -n kube-system svc/headlamp 8000:80
     ```
     Abre **[http://localhost:8000](http://localhost:8000)** y pega el token generado.

### 💻 ¿Prefieres instalarlo como App de Escritorio?
Headlamp también está disponible como aplicación nativa para **Windows**, **macOS** y **Linux** sin necesidad de instalar nada en el clúster. Conoce cómo instalarla en la [Documentación Oficial de Headlamp](https://headlamp.dev/docs/latest/installation/desktop/) o en nuestra [Guía de Headlamp](../headlamp.md).