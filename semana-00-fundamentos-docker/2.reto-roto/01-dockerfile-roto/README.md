# 🎯 Reto 1: El contenedor que se apaga solo al instante (PID 1)

* **Dificultad:** 🟢 Principiante
* **Archivos:** [`Dockerfile`](./Dockerfile) e [`index.html`](./index.html)

---

## 🔍 El Escenario

Un compañero intentó empaquetar una página web usando la imagen oficial de Nginx (`nginx:alpine`).

La construcción de la imagen tiene éxito sin errores:
```bash
docker build -t reto-docker-01 semana-00-fundamentos-docker/2.reto-roto/01-dockerfile-roto
```

Sin embargo, cuando intenta correr el contenedor en segundo plano (`-d`):
```bash
docker run -d -p 8080:80 --name mi-prueba reto-docker-01
```

Y luego revisa con:
```bash
docker ps
```
¡El contenedor **NO aparece en la lista**!

---

## 🕵️‍♂️ Herramientas de Investigación

1. Ejecuta:
   ```bash
   docker ps -a
   ```
   Observa la columna `STATUS`: dirá `Exited (0)` hace pocos segundos.
2. Revisa los logs:
   ```bash
   docker logs mi-prueba
   ```

---

## 💡 ¿Por qué ocurre esto?

En Docker, un contenedor vive **únicamente mientras su proceso principal (PID 1) siga en ejecución**.

Por defecto, el binario `nginx` se ejecuta como demonio en segundo plano (fork) y el comando inicial termina inmediatamente, lo que hace que Docker considere que el trabajo terminó y apague el contenedor.

Para que Nginx mantenga vivo el contenedor, debe ejecutarse en **primer plano** (*foreground*).

---

## 🎯 Tu Misión

1. Abre [`Dockerfile`](./Dockerfile).
2. Modifica la instrucción `CMD` para que Nginx corra en primer plano indicando la directiva de configuración:
   ```dockerfile
   CMD ["nginx", "-g", "daemon off;"]
   ```
3. Vuelve a compilar y ejecutar:
   ```bash
   docker build -t reto-docker-01 semana-00-fundamentos-docker/2.reto-roto/01-dockerfile-roto
   docker run -d -p 8080:80 --name mi-prueba-ok reto-docker-01
   ```
4. Comprueba con `docker ps` que esté en estado `Up` y abre en tu navegador **[http://localhost:8080](http://localhost:8080)**. 🎉
5. Limpia los contenedores de prueba:
   ```bash
   docker rm -f mi-prueba mi-prueba-ok
   ```
