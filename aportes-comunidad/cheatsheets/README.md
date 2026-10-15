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

## 🤝 ¿Cómo aportar tu propio Cheatsheet?

1. Puedes **agregar tus alias o comandos favoritos** directamente en este archivo.
2. O puedes crear un archivo nuevo dentro de esta carpeta (por ejemplo: `comandos-helm.md`, `trucos-k9s.md`, `mi-cheatsheet-tu-usuario.md`).
3. Envía tu **Pull Request** siguiendo la [Guía de Contribución](../../CONTRIBUTING.md) para subir de nivel en [`ASISTENTES.md`](../../ASISTENTES.md).
