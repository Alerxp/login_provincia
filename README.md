# 🔐 Login Provincial con Django

Este proyecto es un microservicio de autenticación desarrollado con Django, que permite a directores de instituciones educativas iniciar sesión con su CUIL y ser redirigidos mediante JWT al sistema nacional.

---

## 🚀 Características principales

- Inicio de sesión seguro con usuario y contraseña (CUIL)
- Redirección al sistema nacional con token JWT firmado
- Panel de administración personalizado con estilos y botón extra
- Vista protegida para importar directores desde archivo CSV
- Listo para despliegue en producción (Gunicorn + Nginx)

---

## ⚙️ 1. Instalación del entorno

```bash
# Clonar el repositorio
git clone https://github.com/Alerxp/login_provincia.git
cd login_provincia

# Crear entorno virtual
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# Instalar dependencias
pip install -r requirements.txt
```

---

## 🛠️ 2. Configuración del entorno

Crear un archivo `.env.production` en la raíz del proyecto con el siguiente contenido:

```env
DEBUG=False
SECRET_KEY=tu_clave_secreta_de_django
JWT_SECRET=clave_compartida_con_sistema_nacional
ALLOWED_HOSTS=login.provincia.gob.ar,127.0.0.1,localhost
LOGIN_REDIRECT_URL=https://censo-demo.die.educacion.gob.ar/relevamientos-docentes
```

---

## 📂 3. Inicialización del proyecto

```bash
# Aplicar migraciones
python manage.py migrate

# Crear superusuario para acceder al panel admin
python manage.py createsuperuser

# Recolectar archivos estáticos (admin, CSS, JS, etc.)
python manage.py collectstatic
```

---

## 🧪 4. Ejecutar en desarrollo (opcional)

```bash
python manage.py runserver
```

Accedé en el navegador a `http://127.0.0.1:8000/admin/`

---

## 🚀 5. Despliegue en producción

1. Ejecutar Gunicorn como servidor WSGI:

```bash
gunicorn loginprovincia.wsgi:application --bind 0.0.0.0:8000
```

2. Configurar Nginx para servir archivos estáticos desde `staticfiles/` y redirigir tráfico al puerto de Gunicorn.

---

## 📁 6. Importar Directores desde CSV

1. Iniciar sesión como superusuario en el panel admin
2. Hacer clic en el botón **“Importar Directores desde CSV”**
3. Subir un archivo `.csv` con este formato:

```
email,cuil,nombre,apellido,cues
```

- `cuil` se usa como usuario y contraseña
- `cues` puede contener varios valores separados por `;`
- Los usuarios existentes se actualizan; los nuevos se crean

---

## 🧾 Archivos importantes

| Archivo                | Descripción                                         |
|------------------------|-----------------------------------------------------|
| `requirements.txt`     | Dependencias del proyecto                           |
| `.env.production`      | Variables de entorno para producción                |
| `loginapp/views.py`    | Lógica de login, generación de JWT, importación     |
| `loginapp/templates/`  | Plantillas personalizadas (admin, login, importar)  |
| `staticfiles/`         | Archivos estáticos recolectados para producción     |

---

## ✅ Estado del proyecto

- [x] Login con CUIL y JWT
- [x] Redirección al sistema nacional
- [x] Administración protegida con Django admin
- [x] Importación segura desde CSV
- [x] Configuración externa vía `.env`
- [x] Preparado para producción

---

## 📄 Licencia

El software es propiedad de **Alexander Nuñez** y se entrega con una licencia de uso **no exclusiva**, intransferible y sin costo al **Área de Evaluación y Estadística Educativa**, dependiente de la **Subsecretaría de Planeamiento Educativo del Ministerio de Educación de la Provincia de San Juan**, República Argentina.

> 📄 Consultar el archivo [`LICENSE.txt`](./LICENSE.txt) para más detalles sobre los términos y condiciones de uso.

Para consultas o autorizaciones, contactarse con el autor: alerxp@gmail.com
