# 🎯 Reto 3: El contenedor vulnerable que corre como root

* **Dificultad:** 🟡 Intermedio
* **Archivo:** [`Dockerfile`](./Dockerfile)

---

## 🔍 El Escenario

La empresa implementó una auditoría estricta de seguridad: **ningún contenedor en producción debe ejecutarse con privilegios de superusuario (`root`)**, ya que si la aplicación sufre una vulnerabilidad de ejecución remota de código, el atacante tendría control absoluto sobre los procesos.

Un compañero empaquetó una API en Python dentro de un contenedor, pero olvidó configurar un usuario sin privilegios.

### 💥 Síntomas

1. Construye la imagen actual:
   ```bash
   docker build -t reto-root:v1.0 semana-00-fundamentos-docker/2.reto-roto/03-contenedor-como-root
   ```
2. Inspecciona qué usuario ejecuta el proceso:
   ```bash
   docker run --rm reto-root:v1.0 whoami
   ```
   *Salida:* `root` ❌ (El proceso corre como UID 0).

3. Al probar con `curl`:
   ```bash
   docker run -d -p 8080:8080 --name test-root reto-root:v1.0
   curl http://localhost:8080
   ```
   *Salida:* `"alerta": "⚠️ ALERTA: Este contenedor está corriendo como superusuario (root)!"`

---

## 🎯 Tu Misión

1. Modifica [`Dockerfile`](./Dockerfile) para aplicar el principio de menor privilegio:
   * Crea un grupo y un usuario no privilegiado en Alpine (por ejemplo `appuser` con UID y GID `10001`):
     ```dockerfile
     RUN addgroup -g 10001 -S appgroup && \
         adduser -u 10001 -S appuser -G appgroup
     ```
   * Asigna la propiedad del archivo copiado al nuevo usuario usando:
     ```dockerfile
     COPY --chown=appuser:appgroup app.py .
     ```
   * Declara la instrucción `USER` antes de `CMD`:
     ```dockerfile
     USER appuser
     ```
2. Vuelve a compilar la imagen:
   ```bash
   docker build -t reto-root:v1.0 semana-00-fundamentos-docker/2.reto-roto/03-contenedor-como-root
   ```
3. Valida que el usuario sea el correcto:
   ```bash
   docker run --rm reto-root:v1.0 whoami
   ```
   *Salida esperada:* `appuser` (o UID 10001) ✅.

4. Corre el contenedor y valida la respuesta HTTP:
   ```bash
   docker run -d -p 8080:8080 --name test-root-ok reto-root:v1.0
   curl http://localhost:8080
   ```
   *Salida esperada:* `"es_root": false` y `"mensaje": "✅ EXCELENTE: El contenedor corre con un usuario sin privilegios."`

5. Limpia los contenedores de prueba:
   ```bash
   docker rm -f test-root test-root-ok
   ```

