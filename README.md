# Sistema de Administración de Biblioteca

Este proyecto es un sistema de administración de una biblioteca desarrollado con Python, Flask, HTML y CSS. Permite gestionar usuarios y libros, así como generar reportes sobre reservas y devoluciones de libros.

## Características

- **Gestión de Usuarios**:

  - Crear nuevos usuarios
  - Editar información de usuarios existentes
  - Eliminar usuarios

- **Gestión de Libros**:

  - Crear nuevos libros
  - Eliminar libros
  - Filtrar por categorias
  - Ordenar libros

- **Reportes**:
  - Generar reportes sobre reservas de libros
  - Generar reportes sobre devoluciones de libros

## Requisitos

- Python 3.x
- Flask
- HTML y CSS

## Instalación

1. Clona este repositorio en tu máquina local:

   ```bash
   git clone https://github.com/tuusuario/sistema-biblioteca.git
   cd sistema-biblioteca
   ```

2. Crea y activa un entorno virtual (opcional pero recomendado):

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
   ```

## Uso

1. Inicia la aplicación:

   ```bash
   py main.py
   ```

2. Abre tu navegador y ve a `http://localhost:5000` para interactuar con el sistema de administración de la biblioteca.

## Estructura del Proyecto

- **app/**: Contiene el código principal de la aplicación.
  - **templates/**: Contiene los archivos HTML.
  - **static/**: Contiene los archivos CSS y otros archivos estáticos.
  - **routes.py**: Define las rutas de la aplicación.
  - **models.py**: Define los modelos de datos.
  - **forms.py**: Define los formularios.
  - **\_\_init\_\_.py**: Inicializa la aplicación y la base de datos.

## Rutas Principales

- `/`: Página de inicio
- `/usuarios`: Lista de usuarios
- `/usuarios/crear`: Crear un nuevo usuario
- `/usuarios/editar/<id>`: Editar un usuario existente
- `/usuarios/eliminar/<id>`: Eliminar un usuario
- `/libros`: Lista de libros
- `/libros/crear`: Crear un nuevo libro
- `/libros/eliminar/<id>`: Eliminar un libro
- `/reportes/reservas`: Generar reporte de reservas de libros
- `/reportes/devoluciones`: Generar reporte de devoluciones de libros
