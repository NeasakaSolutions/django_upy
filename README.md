# 🛡️ Sitio Web de Ingeniería en Ciberseguridad — Universidad Politécnica de Yucatán

# Página segura UPY

### Documentación

---

### Descripción del Proyecto
Este proyecto consiste en el desarrollo de un sitio web diseñado con énfasis en la seguridad, libre de vulnerabilidades conocidas y resistente frente a ataques comunes. Su objetivo principal es promover la carrera de Ingeniería en Ciberseguridad ofrecida por la Universidad Politécnica de Yucatán.

Además, busca generar interés en el público general y proporcionar un espacio donde los estudiantes puedan expresar sus opiniones a través de una sección especialmente habilitada para tal fin.

---
### Tecnologías Utilizadas

- **Python:** Lenguaje de programación principal del backend.

- **Django:** Framework web de alto nivel utilizado para construir el backend de forma segura y estructurada.

- **Django REST Framework:** Extensión de Django que facilita la creación de APIs RESTful.

- **Vue.js:** Framework progresivo de JavaScript utilizado para construir la interfaz de usuario del frontend.

- **Node.js:** Entorno de ejecución para JavaScript utilizado en tareas de compilación, gestión de dependencias del frontend y ejecución de scripts.

- **Bootstrap:** Biblioteca de componentes CSS y JavaScript utilizada para el diseño responsivo y estéticamente coherente.

- **HTML5 y CSS3:** Tecnologías base para la estructura y estilo del sitio web.

- **MySQL:** Sistema de gestión de bases de datos relacional utilizado para almacenar la información de manera eficiente y segura.

- **Cliente MySQL:** Herramienta de línea de comandos o cliente gráfico para administrar la base de datos MySQL.

---
## Dependencias del Proyecto

Para garantizar el correcto funcionamiento de la aplicación, es necesario contar con las siguientes dependencias, tanto a nivel de software como de librerías específicas de Python y herramientas de frontend.

### Dependencias para Backend

- Django 5.1.1

- Django REST Framework 3.15.2

- mysqlclient 2.2.4

- requests 2.31.0

- python-dotenv 1.0.1

- django-autoslug 1.9.9

### Dependencias para Frontend

- Vue.js

- Node.js

- MySQL

- Cliente MySQL

---
### Consideraciones adicionales

- Se recomienda utilizar un entorno virtual (por ejemplo, venv o virtualenv) para aislar las dependencias Python del proyecto y evitar conflictos con otras aplicaciones.

- Para la instalación de las dependencias Python, es preferible usar un archivo requirements.txt que incluya las versiones específicas para mantener consistencia en el entorno de desarrollo y producción.

- La configuración de variables de entorno mediante .env ayuda a mantener datos sensibles fuera del código fuente, como credenciales de base de datos o claves API.

- Para la parte frontend, se sugiere utilizar el gestor de paquetes **npm** (incluido con Node.js) para instalar las dependencias de Vue.js y administrar scripts de compilación o desarrollo.

---

## Instalación y Ejecución

### Crear y activar un entorno virtual

Todos los comandos deben ejecutarse desde una terminal, ya sea la integrada en Visual Studio Code o la del sistema operativo.

- Verificar si **virtualenv** está instalado:

``` bash
virtualenv --version
```

- Instalar virtualenv si no está disponible:

``` bash
pip install virtualenv
```

- Crear el entorno virtual (este paso puede tardar unos segundos):

``` bash
virtualenv venv
```

- Activar el entorno virtual en Windows:

``` bash
source env/bin/activate  # En Linux/macOS
.\venv\Scripts\activate # En Windows
```

### Instalar las dependencias

- Ejecuta

``` bash
pip install -r requirements.txt
```

### Configurar variables de entorno

- Crea un archivo .env en la raíz del proyecto Django con variables sensibles, por ejemplo:

``` bash
DEBUG=True
SECRET_KEY=tu_clave_secreta
DB_NAME=nombre_basedatos
DB_USER=usuario
DB_PASSWORD=contraseña
DB_HOST=localhost
DB_PORT=3306
```

### Aplicar migraciones y ejecutar el servidor

```bash
python manage.py migrate
python manage.py runserver
```

### Instalar dependencias del frontend

- Asegúrate de tener Node.js y npm instalados:

``` bash
node -v
npm -v
```

- Luego, navega a la carpeta del frontend (por ejemplo, /frontend) y ejecuta:

``` bash
npm install
```
- Esto instalará todas las dependencias definidas en el archivo package.json.

- Ejecutar servidor de desarrollo:

``` bash
npm run dev -- --host
```
---
## Estructura del proyecto

- Fronted

```bash
frontend/
│
├── .vscode/               # Configuración específica para Visual Studio Code.
├── node_modules/          # Dependencias instaladas con npm. (No editar manualmente)
├── public/                # Archivos públicos accesibles directamente (favicon, index.html si aplica, etc.).
├── src/                   # Código fuente de la aplicación (componentes, vistas, estilos, etc.).
│
├── .gitattributes         # Define cómo Git trata ciertos archivos (como texto, binario, etc.).
├── .gitignore             # Lista de archivos y carpetas que Git debe ignorar.
├── eslint.config.js       # Configuración de ESLint para análisis de código.
├── index.html             # Archivo HTML principal de la aplicación.
├── jsconfig.json          # Configuración de rutas y alias para JavaScript en el proyecto.
├── package-lock.json      # Registro exacto de versiones de dependencias (autogenerado por npm).
├── package.json           # Define las dependencias, scripts y configuración del proyecto.
├── README.md              # Documentación del proyecto.
└── vite.config.js         # Configuración del bundler Vite para el entorno de desarrollo.
```

- Fronted/public

``` bash
public/
│
├── css/                 # Estilos de Bootstrap y estilos personalizados.
├── fonts/               # Iconos y tipografías utilizadas en el sitio.
├── img/                 # Recursos gráficos de la página.
│   ├── bg_img/          # Imágenes de fondo utilizadas en el diseño.
│   ├── blog_image/      # Imágenes generales para entradas de blog o contenido dinámico.
│   ├── core_img/        # Logotipos principales del sitio web.
│   ├── gif/             # Archivos animados en formato GIF.
│   ├── img/             # Imágenes especiales o de propósito específico.
│   └── svg_logos/       # Logos en formato SVG.
│
├── js/                  # Lógica JavaScript de Bootstrap y scripts personalizados.
├── scss/                # Archivos fuente de estilos en Sass (SCSS).
├── style.css            # Hoja de estilos compilada principal.
├── style.css.map        # Archivo de mapeo para facilitar la depuración de estilos SCSS.
```

- Fronted/src

```bash
src/
│
├── assets/              # Recursos multimedia adicionales (imágenes, videos, íconos, etc.).
│
├── components/          # Componentes reutilizables (HTML/JSX/Vue) de la interfaz.
│   ├── Fondo.vue        # Componente con fondo animado.
│   ├── Footer.vue       # Componente del pie de página.
│   └── Header.vue         # Componente del menú de navegación superior.
│
├── router/              # Configuración de rutas entre páginas.
│   └── index.js         # Archivo que define las rutas de navegación de la aplicación.
│
├── stores/              # (Opcional) Estado global de la aplicación, usando Pinia o Vuex.
│
├── views/               # Vistas principales (equivalentes a páginas).
│   ├── Videos.vue       # Componente que muestra la sección de videos.
│   └── Home.vue         # Vista principal que incluye o coordina otras secciones.
│
├── App.vue              # Componente raíz de la aplicación Vue.
└── main.js              # Punto de entrada de la aplicación. Inicializa Vue y monta la app.
```


---

1. Clona el repositorio:
   ```bash
    git clone https://github.com/NeasakaSolutions/Pagina_segura_UPY.git
    cd Pagina_segura_UPY