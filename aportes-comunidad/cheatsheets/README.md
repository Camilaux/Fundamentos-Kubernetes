# 🧰 Cheatsheets de la Comunidad — Cloud Native Medellín

¡Bienvenido al baúl de trucos, atajos y comandos salvavidas de la comunidad! 

Aquí compartimos los comandos que usamos en el día a día para no tener que memorizar sintaxis complejas ni escribir comandos largos mil veces.

---

## ⚡ Atajos y Alias Esenciales (Shell / Bash / Zsh)

Agrega estos alias a tu `~/.bashrc` o `~/.zshrc` para multiplicar tu velocidad en la terminal:

```bash
# Navegación básica
alias k='kubectl'
alias kgp='kubectl get pods'
alias kgs='kubectl get services'
alias kgn='kubectl get nodes'
alias kgd='kubectl get deployments'

# Inspección rápida
alias kdp='kubectl describe pod'
alias kdn='kubectl describe node'
alias kds='kubectl describe service'

# Logs en vivo
alias kl='kubectl logs -f'
alias klp='kubectl logs --previous'

# Ejecutar comandos dentro de un contenedor
alias kexec='kubectl exec -it'

# Aplicar o borrar manifiestos
alias kaf='kubectl apply -f'
alias kdf='kubectl delete -f'

# Cambio rápido de namespace (si usas kubens o kubectl)
alias kctx='kubectx'
alias kns='kubens'
```

---

## 🔍 Comandos de Supervivencia: Depuración Rápida

| ¿Qué quiero hacer? | Comando |
| :--- | :--- |
| **Ver Pods ordenados por nodo** | `kubectl get pods -o wide` |
| **Ver eventos ordenados cronológicamente** | `kubectl get events --sort-by='.metadata.creationTimestamp'` |
| **Ver por qué un Pod no arranca** | `kubectl describe pod <nombre-pod>` *(mira la sección Events al final)* |
| **Ver logs del contenedor anterior antes de caerse** | `kubectl logs <nombre-pod> --previous` |
| **Abrir una terminal temporal para probar red dentro del clúster** | `kubectl run test-net --rm -i --tty --image=nicolaka/netshoot -- /bin/bash` |
| **Ver consumo de CPU y RAM de los nodos** | `kubectl top nodes` *(requiere metrics-server)* |
| **Ver consumo de CPU y RAM de los Pods** | `kubectl top pods` *(requiere metrics-server)* |

---

## 🐳 Atajos y Comandos de Docker (Fundamentos para K8s)

```bash
# Alias útiles para Docker
alias d='docker'
alias dps='docker ps'
alias dpsa='docker ps -a'
alias di='docker images'
alias dl='docker logs -f'
alias dexec='docker exec -it'
alias dstop='docker stop'
alias drm='docker rm'
alias drmi='docker rmi'
alias dprune='docker system prune -f'
```

| ¿Qué quiero hacer con Docker? | Comando |
| :--- | :--- |
| **Construir imagen desde Dockerfile actual** | `docker build -t mi-app:v1.0 .` |
| **Correr contenedor mapeando puerto** | `docker run -d -p 8080:80 --name mi-app mi-app:v1.0` |
| **Entrar a la terminal interactiva del contenedor** | `docker exec -it mi-app sh` |
| **Ver logs en tiempo real** | `docker logs -f mi-app` |
| **Inyectar imagen local a tu clúster de Kind** | `kind load docker-image mi-app:v1.0 --name cnm-lab` |
| **Limpiar contenedores detenidos e imágenes huérfanas** | `docker system prune` |

---

## 🐝 Kind & Cilium Tips

```bash
# Ver clústeres de Kind activos
kind get clusters

# Eliminar un clúster para liberar memoria RAM
kind delete cluster --name <nombre-cluster>

# Inspeccionar el estado de Cilium y eBPF
cilium status

# Probar la conectividad completa entre Pods gestionados por Cilium
cilium connectivity test
```

---

## 🌐 Entornos de Práctica Interactivos (Playgrounds en la Nube)

¿Sin acceso a tu terminal o tu máquina no tiene Docker/Kind instalado? Practica con estos laboratorios interactivos gratuitos directamente en el navegador:

* 🐳 **Laboratorios de Docker:** [KodeKloud Studio — Docker](https://kodekloud.com/studio/labs/docker)
* ☸️ **Laboratorios de Kubernetes:** [KodeKloud Studio — Kubernetes](https://kodekloud.com/studio/labs/kubernetes)

---

## 🤝 ¿Cómo aportar tu propio Cheatsheet?

1. Puedes **agregar tus alias o comandos favoritos** directamente en este archivo.
2. O puedes crear un archivo nuevo dentro de esta carpeta (por ejemplo: `comandos-helm.md`, `trucos-k9s.md`, `mi-cheatsheet-tu-usuario.md`).
3. Envía tu **Pull Request** siguiendo la [Guía de Contribución](../../CONTRIBUTING.md) para subir de nivel en [`ASISTENTES.md`](../../ASISTENTES.md).
