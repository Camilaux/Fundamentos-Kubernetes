# 🎯 Reto 2: El contenedor que crashea por falta de variable de entorno (`ENV`)

* **Dificultad:** 🟢 Principiante
* **Archivos:** [`Dockerfile`](./Dockerfile) y [`app.py`](./app.py)

---

## 🔍 El Escenario

Un compañero creó un microservicio que requiere una variable de entorno obligatoria llamada `APP_SECRET_TOKEN` para conectarse a un servicio central y autenticar peticiones.

Construyes la imagen exitosamente:
```bash
docker build -t reto-docker-02 semana-00-fundamentos-docker/2.reto-roto/02-variable-entorno-faltante
```

La ejecutas en segundo plano con:
```bash
docker run -d -p 8080:8080 --name mi-api-02 reto-docker-02
```

Pero al revisar con `docker ps`, **el contenedor no aparece en la lista de activos**.

---

## 🕵️‍♂️ Herramientas de Investigación

1. Revisa los contenedores detenidos:
   ```bash
   docker ps -a
   ```
   Verás que `mi-api-02` terminó con código de salida `Exited (1)`.
2. Lee los logs del contenedor para saber qué falló:
   ```bash
   docker logs mi-api-02
   ```
   *Salida:*  
   `💥 ERROR FATAL: La variable de entorno obligatoria 'APP_SECRET_TOKEN' no fue proporcionada.`

---

## 💡 ¿Por qué ocurre esto?

En Docker, una aplicación empaquetada dentro de una imagen no hereda automáticamente las variables de entorno de tu máquina local. Para que una variable exista dentro del contenedor, debe ser:
1. Definida como valor por defecto dentro del `Dockerfile` usando la instrucción `ENV`.
2. O inyectada en tiempo de ejecución mediante la bandera `-e` de `docker run`.

---

## 🎯 Tu Misión (Tienes 2 formas de resolverlo)

* **Solución 1 (Desde el Dockerfile):**  
  Abre [`Dockerfile`](./Dockerfile) y agrega una variable por defecto:
  ```dockerfile
  ENV APP_SECRET_TOKEN="token-local-dev-12345"
  ```
  Vuelve a construir y ejecutar:
  ```bash
  docker build -t reto-docker-02 semana-00-fundamentos-docker/2.reto-roto/02-variable-entorno-faltante
  docker run -d -p 8080:8080 --name mi-api-02 reto-docker-02
  ```

* **Solución 2 (En tiempo de ejecución con `docker run -e`):**  
  Pasa la variable directamente al arrancar el contenedor sin tocar el `Dockerfile`:
  ```bash
  docker run -d -p 8080:8080 -e APP_SECRET_TOKEN="mi-token-dinamico" --name mi-api-02 reto-docker-02
  ```

### Validación
Verifica con `curl http://localhost:8080` o abre en tu navegador. Recibirás un JSON confirmando:
```json
{
  "estado": "activo",
  "mensaje": "🎉 ¡Excelente! La variable de entorno fue configurada correctamente.",
  "token_configurado": "...",
  "puerto": 8080
}
```

Al terminar, limpia el contenedor:
```bash
docker rm -f mi-api-02
```
