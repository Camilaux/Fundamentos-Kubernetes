# 🎯 Reto 5: El puerto fantasma y la trampa del localhost (`127.0.0.1` vs `0.0.0.0`)

* **Dificultad:** 🟢 Principiante / 🟡 Intermedio
* **Archivos:** [`Dockerfile`](./Dockerfile) y [`app.py`](./app.py)

---

## 🔍 El Escenario

Un compañero creó un microservicio en Python y lo empaquetó con Docker. Al ejecutarlo con `docker run -d -p 8080:8080`, el comando tiene éxito y `docker ps` muestra que el contenedor está en estado `Up` (corriendo).

Sin embargo, cuando intenta abrir **`http://localhost:8080`** en el navegador o ejecutar `curl http://localhost:8080`:
```text
curl: (52) Empty reply from server
# o bien:
curl: (7) Failed to connect to localhost port 8080: Connection refused
```

### 💥 ¿Por qué ocurre esto? (Las 2 causas más comunes)

1. **La trampa de `127.0.0.1` vs `0.0.0.0`:**  
   Dentro de un contenedor, `127.0.0.1` representa la interfaz de *loopback* interna de ese contenedor aislado. Si la aplicación se enlaza solo a `127.0.0.1`, **rechazará cualquier conexión que venga desde fuera del contenedor**. Para aceptar conexiones externas reenviadas por Docker, la aplicación debe escuchar en `0.0.0.0` (todas las interfaces de red del contenedor).
2. **Desalineación de puertos:**  
   Si la aplicación escucha en un puerto (ej. `5000`) pero Docker mapea otro (ej. `8080:8080`), el tráfico nunca llegará al proceso.

---

## 🎯 Tu Misión

1. Abre [`app.py`](./app.py) e investiga los valores de `HOST` y `PORT`.
2. Corrige `app.py` para que:
   * Escuche en `0.0.0.0`.
   * El puerto coincida con el puerto expuesto y mapeado (`8080`).
3. Revisa [`Dockerfile`](./Dockerfile) para asegurarte de que `EXPOSE` documente el puerto correcto.
4. Construye y corre la imagen:
   ```bash
   docker build -t reto-puerto:v1.0 semana-00-fundamentos-docker/2.reto-roto/05-puerto-y-host-desalineado
   docker run -d -p 8080:8080 --name reto-puerto-test reto-puerto:v1.0
   ```
5. Prueba con `curl http://localhost:8080`.  
   ¡Debes recibir el JSON de éxito con `"estado": "conectado"`! 🎉
6. Al finalizar, limpia el contenedor:
   ```bash
   docker stop reto-puerto-test && docker rm reto-puerto-test
   ```
