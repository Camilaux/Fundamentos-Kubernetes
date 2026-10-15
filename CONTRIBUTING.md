# 🤝 Guía para contribuir a Fundamentos-Kubernetes

¡Qué alegría que quieras aportar! Aquí **cualquier mejora cuenta**: desde agregarte a la lista de asistentes hasta resolver un laboratorio complejo.

Si nunca has hecho un **Pull Request (PR)** en GitHub, sigue estos pasos sencillos:

---

## 🎯 3 formas fáciles de empezar hoy mismo

1. **Tu primer PR en 5 minutos (`ASISTENTES.md`):** Abre el archivo `ASISTENTES.md` y agrega tu nombre al final de la tabla.
2. **Solucionar un "Reto Roto":** Cada semana tiene una carpeta `reto-roto/` con archivos YAML que fallan a propósito.
   * ⚠️ **Regla de oro:** ¡No modifiques los archivos originales de `reto-roto/`!
   * Crea una carpeta con tu usuario en `aportes-comunidad/soluciones-retos/tu-usuario/semana-01/` y pega ahí tu YAML corregido explicando en un comentario (`#`) cuál era el error.
3. **Compartir trucos o apuntes:** Sube tus resúmenes o comandos favoritos en `aportes-comunidad/cheatsheets/`.

---

## 🚀 Paso a paso: Cómo enviar tus cambios (Pull Request)

### Paso 1: Haz un "Fork" (Tu copia personal)
Arriba a la derecha en la página principal de [edwinbermudez91/Fundamentos-Kubernetes](https://github.com/edwinbermudez91/Fundamentos-Kubernetes), haz clic en el botón **Fork**.

### Paso 2: Descarga tu copia a tu computador (Clone)
Abre tu terminal y ejecuta (reemplaza `TU-USUARIO` por tu usuario de GitHub):

```bash
git clone [https://github.com/TU-USUARIO/Fundamentos-Kubernetes.git](https://github.com/TU-USUARIO/Fundamentos-Kubernetes.git)
cd Fundamentos-Kubernetes
```

### Paso 3: Crea una rama nueva (Branch)
```bash
git checkout -b mi-aporte-semana-1
```

### Paso 4: Guarda tus cambios (Commit)
Haz tus cambios y guárdalos con estos comandos:

```bash
git add .
git commit -m "Agrega mi nombre en ASISTENTES y solucion semana 1"
```

### Paso 5: Sube los cambios a tu GitHub (Push)
```bash
git push origin mi-aporte-semana-1
```

### Paso 6: Abre el Pull Request
Entra a tu repositorio en GitHub desde el navegador y haz clic en el botón verde **"Compare & pull request"** -> **"Create pull request"**. ¡Listo! 🎉
