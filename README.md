# Sistema de Gestión de Laboratorio Electrónico

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Django](https://img.shields.io/badge/Django-4.2-green)
![SQLite](https://img.shields.io/badge/SQLite-3.0-blue)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)

Sistema completo para la gestión de inventario, usuarios y préstamos en laboratorios de electrónica universitaria. Permite a encargados administrar componentes y solicitudes, y a estudiantes consultar y solicitar materiales con seguimiento automatizado.

---

## Características Principales

- **Gestión de inventario avanzada** con categorización por tags
- **Edición visual de componentes** con validación por contraseña
- **Sistema de usuarios** con roles diferenciados y edición de perfil
- **Gestión de archivos** para imágenes y datasheets
- **Vista detallada con modal dinámico** para cada componente
- **Interfaz responsiva** con Bootstrap y templates HTML
- **Autenticación personalizada** con cédula como identificador

---

## Tecnologías Utilizadas

| Área           | Tecnologías                          |
|----------------|--------------------------------------|
| Frontend       | HTML, CSS, Bootstrap 5               |
| Backend        | Django 4.2 (Python)                  |
| Base de Datos  | SQLite 3                             |
| Autenticación  | Django Auth personalizado            |
| Almacenamiento | Sistema de archivos local (media/)   |

---

## Estructura del Proyecto

```
ElectronicLab/
├── ElectronicLabWeb/
│   ├── core/
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── templates/
│   │       └── core/
│   │           └── home.html
│   │
│   ├── ElectronicLabWeb/
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   │
│   ├── files/             # Manejo de archivos (imagen, PDF)
│   │   ├── admin.py
│   │   ├── models.py
│   │   └── serializers.py # API para guardar archivos
│   │
│   ├── inventory/         # Gestión de componentes
│   │   ├── admin.py
│   │   ├── models.py      # Componentes, categorías, archivos
│   │   ├── views.py       # CRUD, vista detallada, migración
│   │   ├── forms.py       # Formularios de creación y edición
│   │   ├── urls.py
│   │   ├── management
│   │   │   └── commands
│   │   │       └── clean_orphans.py
│   │   │
│   │   └── templates/
│   │       └── inventory/ # Templates de inventario
│   │           ├── component_edit.html
│   │           ├── component_form.html
│   │           └── component_list.html
│   │
│   ├── static/            # Archivos JS y CSS personalizados
│   │   ├── css/
│   │   │   └── base.css
│   │   │
│   │   ├── img/
│   │   │   ├── bg-dark.jpg
│   │   │   ├── bg-light.jpg
│   │   │   ├── default-user.png
│   │   │   ├── no-image.png
│   │   │   └── unexpo-logo.png
│   │   │
│   │   └── js/            # tagSelector.js, editGuard.js, etc.
│   │       ├── base.js
│   │       ├── componentDetail.js
│   │       ├── deleteModal.js
│   │       ├── editGuard.js
│   │       └── tagSelector.js
│   │
│   ├── templates/         # Base general y barra de navegación
│   │   ├── base.html
│   │   ├── navbar.html
│   │   └── sidebar_items.html
│   │
│   ├── users/             # Gestión de usuarios y autenticación
│   │   ├── admin.py
│   │   ├── models.py      # Modelo personalizado de usuario
│   │   ├── views.py       # Login, logout, perfil, edición
│   │   ├── forms.py       # Formularios de perfil y edición
│   │   ├── urls.py
│   │   ├── managers.py
│   │   └── templates/
│   │       └── users/     # Templates de login, perfil, edición
│   │           ├── login.html
│   │           ├── profile_edit.html
│   │           └── profile.html
│   │
│   ├── .env
│   ├── db.sqlite3
│   ├── manage.py
│   └── requeriments.txt  
│
└── media/             # Archivos subidos por los usuarios
    └── uploads/
        ├── originals
        ├── previews
        └── thumbnails
```

---

### Entidades Principales

- **Usuario**: Cédula, nombre, apellido, email, telefono, rol, estado, foto
- **Componente**: Código, descripción, stock, ubicación, imagen, datasheet
- **Categoría**: Sistema de tags para clasificar componentes
- **Archivo**: Imagen o PDF vinculado a un componente o usuario

---

## Instalación y Configuración

### Requisitos Previos

- Python 3.9+
- pip
- SQLite (incluido por defecto)

### Pasos de Instalación

1. Clonar repositorio:
```bash
git clone https://github.com/Gardic-Coder/ElectronicLab.git
cd ElectronicLab
```

2. Configurar entorno:
```bash
# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac)
venv\Scripts\activate    # Windows

# Instalar dependencias
pip install -r requirements.txt
```

3. Configurar variables de entorno:
- Crear archivo `.env` en la raíz del proyecto:
```ini
# Seguridad
SECRET_KEY=tu_clave_secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Archivos
MEDIA_URL=/media/
MEDIA_ROOT=tu_ruta_de_la_carpeta_media
ALLOWED_MIME_TYPES=image/jpeg,image/png,application/pdf
```

4. Inicializar base de datos:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Crear superusuario:
```bash
python manage.py createsuperuser
```

6. Ejecutar servidor:
```bash
python manage.py runserver
# O para poder probarlo tambien en moviles y otros dispositivos conectados a la misma red
python manage.py runserver 0.0.0.0:8000
```

---

## Estado Actual del Proyecto

### ✅ Funcionalidades Completadas

- Autenticación personalizada con cédula
- Edición de perfil con validación por contraseña
- CRUD completo de componentes
- Vista detallada con modal dinámico
- Carga y eliminación de imagen/datasheet
- Categorización por tags con buscador interactivo

### ⏳ En Progreso

- Solicitud y aprobación de préstamos
- Panel de efemérides técnicas

### 📅 Próximas Funcionalidades

- Registro de devoluciones y penalizaciones
- Auditoría de operaciones
- Notificaciones por email
- Dashboard con métricas
- Integración con sistemas universitarios
- App móvil complementaria

---

## Capturas de Pantalla

*(Se agregarán cuando la interfaz esté más desarrollada)*

---

## Licencia

Este proyecto está bajo la licencia [MIT](LICENSE).

---