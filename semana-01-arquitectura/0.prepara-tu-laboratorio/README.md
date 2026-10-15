## 🐳 ¿Qué es Kind y por qué lo usamos en el Workshop?

**Kind** significa **K**ubernetes **in** **D**ocker. 

Tradicionalmente, para tener un clúster de Kubernetes en tu computador necesitabas crear varias máquinas virtuales pesadas que consumían toda tu memoria RAM. **Kind hace trampa (de la buena):** simula cada servidor de Kubernetes (*Nodo*) usando un simple contenedor de Docker. Es súper rápido, ligero y se borra en segundos sin dejar basura en tu sistema.

### ⚡ Comandos básicos de Kind que usarás todos los días

```bash
# 1. Crear un clúster sencillo (1 solo nodo) con nombre personalizado
kind create cluster --name cnm-lab

# 2. Ver cuántos clústeres de Kind tienes creados
kind get clusters

# 3.Crear un clúster personalizado usando un archivo YAML (¡Lo haremos abajo!)
kind create cluster --name cnm-pro --config setup-local/kind-multinode.yaml

# 4. Borrar un clúster cuando termines de practicar (libera tu RAM)
kind delete cluster --name cnm-lab
```

---

## 🛠️ Personalizando tu Clúster de Kind con YAML

Por defecto, Kind crea un solo servidor que hace de jefe (*Control Plane*) y obrero (*Worker*) al mismo tiempo. En la carpeta [`/setup-local`](./setup-local) tienes plantillas YAML para crear clústeres como en el mundo real:

<details>
<summary><b>📄 1. Clúster Multi-Nodo (1 Cerebro + 2 Obreros) — <code>setup-local/kind-multinode.yaml</code></b></summary>
<br>

Ideal para ver cómo Kubernetes reparte tus Pods en distintos servidores:

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  # El cerebro del clúster
  - role: control-plane
  # Los servidores obreros donde correrán tus aplicaciones
  - role: worker
  - role: worker
```
**Cómo crearlo:**
```bash
kind create cluster --name cnm-multinodo --config setup-local/kind-multinode.yaml
```
</details>

<details>
<summary><b>🌐 2. Clúster listo para Ingress (Puertos 80 y 443 abiertos) — <code>setup-local/kind-ingress.yaml</code></b></summary>
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
kind create cluster --name cnm-redes --config setup-local/kind-ingress.yaml
```
</details>

---

## 🧰 Kit de Supervivencia: Si tienes varios clústeres

Cuando tienes el clúster del trabajo, el de pruebas y el del workshop al mismo tiempo, es muy fácil equivocarse y lanzar un comando donde no debes. Estas **4 herramientas gratuitas** te harán la vida mucho más fácil:

| Herramienta | ¿Para qué sirve en palabras sencillas? | Cómo se usa |
| :--- | :--- | :--- |
| **[kubectx](https://github.com/ahmetb/kubectx)** | **El control remoto de clústeres.** Te permite saltar de un clúster a otro en 1 segundo sin comandos largos. | `kubectx` *(lista tus clústeres)*<br>`kubectx kind-cnm-lab` *(cambia de clúster)*<br>`kubectx -` *(vuelve al clúster anterior)* |
| **[kubens](https://github.com/ahmetb/kubectx)** | **El selector de carpetas (Namespaces).** Se instala junto con `kubectx` y te ahorra escribir `-n mi-namespace` en cada comando. | `kubens` *(lista los namespaces)*<br>`kubens kube-system` *(entra a ese namespace)* |
| **[k9s](https://k9scli.io/)** | **El panel de control en tu terminal.** Es una interfaz visual interactiva dentro de la consola para ver logs, entrar a Pods y borrar recursos con atajos de teclado. | Solo escribe `k9s` en tu terminal y muévete con las flechas. |
| **[stern](https://github.com/stern/stern)** | **El megáfono de logs.** Te permite ver los logs de muchos Pods al mismo tiempo y con colores distintos. | `stern mi-app` *(muestra los logs en vivo de todas las réplicas de tu app)*. |

> [!TIP]
> **El truco de velocidad número 1:** Agrega un alias en tu terminal para no escribir `kubectl` completo mil veces.
> Ejecuta `alias k=kubectl` y ahora podrás escribir simplemente `k get pods` o `k describe pod mi-pod`.