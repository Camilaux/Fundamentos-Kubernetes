# 💾 Ejemplo 04: Almacenamiento y Volúmenes en Docker

En este laboratorio aprenderás la diferencia crítica entre el **almacenamiento efímero** de un contenedor y el **almacenamiento persistente** con **Named Volumes** y **Bind Mounts**.

---

## ☕ La Analogía Paisa: El Libro Contable del Carrito

Un carrito de tintos en el Metro es reemplazable: si una llanta se pincha o la greca se apaga, cambias el carrito (`docker rm` y `docker run`).  
Pero la **libreta de ventas** (`ventas.json`) donde anotas a quién le fías y cuánto vendiste en el día **no puede quemarse con el carrito**.

* **Sin volumen (Efímero):** Si guardas las notas dentro de la gaveta del carrito viejo y botas el carrito a la basura... ¡perdiste las cuentas!
* **Con Named Volume (`docker volume`):** Es una caja fuerte independiente administrada por Docker. Destruyes el carrito, compras uno nuevo, le montas la caja fuerte y ¡todas las ventas siguen ahí!
* **Con Bind Mount (`-v host:cont`):** Es tener la libreta física en tu escritorio de la casa conectada por un cable directo al carrito. Puedes editar el archivo desde tu computador (con VS Code) y el contenedor lo lee de inmediato.

---

## 🔬 Los Experimentos Prácticos y Auditoría de Seguridad

### Paso 0: Construir la imagen
Desde la raíz del repositorio:

```bash
docker build -t app-ventas:v1.0 semana-00-fundamentos-docker/1.ejemplos/04-almacenamiento-y-volumenes
```

---

### 🧪 Experimento 1: Sin Volumen (La Tragedia de los Datos Efímeros)

1. Corre el contenedor **sin montar volúmenes**:
   ```bash
   docker run -d -p 8080:8080 --name test-efimero app-ventas:v1.0
   ```

2. Registra ventas:
   * Abre **[http://localhost:8080](http://localhost:8080)** y haz clic en *"Registrar Venta de Tinto"* varias veces.
   * O por terminal:
     ```bash
     curl "http://localhost:8080/vender?tipo=Tinto+Campesino&cliente=Carlos"
     curl "http://localhost:8080/vender?tipo=Perico&cliente=Mariana"
     curl http://localhost:8080/api
     ```

3. Ahora simula un fallo y destruye el contenedor:
   ```bash
   docker rm -f test-efimero
   ```

4. Vuelve a crear el contenedor:
   ```bash
   docker run -d -p 8080:8080 --name test-efimero app-ventas:v1.0
   curl http://localhost:8080/api
   ```
   💥 **Resultado:** `"total_registros": 0`. **¡Todos los datos se perdieron para siempre!** La capa de escritura del contenedor murió con él.

Limpia el contenedor de prueba:
```bash
docker rm -f test-efimero
```

---

### 🧪 Experimento 2: Con Named Volume (Persistencia Real)

Los **Named Volumes** son administrados por el Docker Engine en una zona aislada y segura del disco del host.

1. Crea el volumen dedicado:
   ```bash
   docker volume create datos-tintos
   ```

2. Inspecciona el volumen:
   ```bash
   docker volume inspect datos-tintos
   ```

3. Inicia un contenedor montando el volumen en `/app/datos`:
   ```bash
   docker run -d -p 8080:8080 \
     --name carrito-1 \
     -v datos-tintos:/app/datos \
     app-ventas:v1.0
   ```

4. Registra nuevas ventas:
   ```bash
   curl "http://localhost:8080/vender?tipo=Tinto+Especial+Paisa&cliente=Don+Guillermo"
   curl "http://localhost:8080/vender?tipo=Cafe+de+Origen&cliente=Sofia"
   curl http://localhost:8080/api
   ```

5. **¡Destruye el contenedor sin piedad!**
   ```bash
   docker rm -f carrito-1
   ```

6. Crea un contenedor COMPLETAMENTE NUEVO (`carrito-2`) usando el mismo volumen:
   ```bash
   docker run -d -p 8080:8080 \
     --name carrito-2 \
     -v datos-tintos:/app/datos \
     app-ventas:v1.0
   ```

7. Consulta los datos del nuevo contenedor:
   ```bash
   curl http://localhost:8080/api
   ```
   🎉 **Resultado:** ¡Todas las ventas de Don Guillermo y Sofía siguen intactas! Observa que el campo `hostname_contenedor` muestra qué contenedor específico generó cada registro.

Limpia el contenedor:
```bash
docker rm -f carrito-2
```

---

### 🧪 Experimento 3: Con Bind Mount (Sincronización en Vivo con tu Máquina)

Un **Bind Mount** conecta directamente una carpeta de tu máquina anfitrión (Host) con una ruta dentro del contenedor. Es ideal para desarrollo local.

1. Crea una carpeta local en tu máquina y dale permisos de escritura para el usuario sin privilegios del contenedor (`appuser`, UID 10001):
   ```bash
   mkdir -p ./mis-datos-locales
   chmod 777 ./mis-datos-locales
   ```

2. Corre el contenedor montando esa carpeta usando ruta absoluta con `$(pwd)`:
   ```bash
   docker run -d -p 8080:8080 \
     --name carrito-bind \
     -v "$(pwd)/mis-datos-locales:/app/datos" \
     app-ventas:v1.0
   ```

3. Registra una venta:
   ```bash
   curl "http://localhost:8080/vender?tipo=Tinto+con+Panela&cliente=Estudiante+Cloud+Native"
   ```

4. Inspecciona el archivo directamente desde tu propia máquina:
   ```bash
   cat ./mis-datos-locales/ventas.json
   ```
   ✨ **¡Magia!** El archivo existe en tu disco local. Si editas `ventas.json` desde tu editor de código o terminal, el contenedor verá el cambio en tiempo real.

---

### 🧪 Experimento 4: Auditoría de Seguridad con Trivy (CLI)

En aplicaciones con almacenamiento de datos persistentes (como `ventas.json`), la seguridad del contenedor es fundamental. Ejecuta el análisis de la imagen y de las instrucciones de construcción directamente desde tu línea de comandos con el paquete `trivy`:

```bash
# 1. Escanear vulnerabilidades conocidas (CVEs) en la imagen:
trivy image --severity HIGH,CRITICAL app-ventas:v1.0

# 2. Auditar buenas prácticas en el Dockerfile:
trivy config semana-00-fundamentos-docker/1.ejemplos/04-almacenamiento-y-volumenes

# Alternativa mediante contenedor efímero si no tienes el paquete instalado:
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image --severity HIGH,CRITICAL app-ventas:v1.0
```

> 🛡️ **Resultado esperado:** La imagen reportará **0 vulnerabilidades de severidad alta o crítica**. Al separar los datos en volúmenes y mantener la imagen inmutable y limpia, tu aplicación cumple con los estándares para Kubernetes. Consulta la [Guía de Seguridad con Trivy](../../../recursos/guia-trivy-seguridad.md).

---

### Limpieza Final
```bash
docker rm -f carrito-bind
docker volume rm datos-tintos
rm -rf ./mis-datos-locales
```

---

## 🌉 El Puente a Kubernetes: ¿Cómo se traduce esto?

| En Docker | En Kubernetes | Explicación |
| :--- | :--- | :--- |
| **Capa de contenedor (sin volumen)** | **`emptyDir: {}`** | Almacenamiento temporal que se borra al morir el Pod. |
| **Bind Mount (`-v $(pwd):/cont`)** | **`hostPath`** | Monta una carpeta del nodo físico en el Pod (usado en DaemonSets y Kind). |
| **Named Volume (`docker volume`)** | **`PersistentVolume (PV)` + `PVC`** | Almacenamiento desacoplado del ciclo de vida del Pod (disco en la nube: AWS EBS, Azure Disk, NFS, etc.). |
| Docker Volume Driver | **`StorageClass` + CSI** | Aprovisiona discos automáticamente cuando un Pod lo solicita. |
