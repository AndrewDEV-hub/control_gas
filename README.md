# Proyecto Control de Carga de Combustible

Este proyecto es una aplicación web desarrollada con Flask que permite registrar, controlar y supervisar la carga de combustible de vehículos. Incluye dos usuarios principales, registrador y supervisor, control de restricciones por día y terminación de CI, restricciones de cantidad de litros cargados por mes, generación y escaneo de códigos QR.

## 📂 Estructura base del proyecto
```
control_gas
├─ add_default_estaciones.py
├─ add_default_users.py
├─ app.py
├─ controllers
│  ├─ auth_controlador.py
│  ├─ carga_combustible_controlador.py
│  ├─ estacion_controlador.py
│  ├─ funcionario_publico_controlador.py
│  ├─ persona_controlador.py
│  ├─ persona_vehiculo_controlador.py
│  ├─ restriccion_dia_controlador.py
│  ├─ usuario_controlador.py
│  ├─ vehiculo_controlador.py
│  ├─ vehiculo_institucional.py
│  ├─ __init__.py
│  └─ __pycache__
│     ├─ auth_controlador.cpython-313.pyc
│     ├─ carga_combustible_controlador.cpython-313.pyc
│     ├─ combustible_controlador.cpython-313.pyc
│     ├─ estacion_controlador.cpython-313.pyc
│     ├─ funcionario_publico_controlador.cpython-313.pyc
│     ├─ persona_controlador.cpython-313.pyc
│     ├─ persona_vehiculo_controlador.cpython-313.pyc
│     ├─ restriccion_dia_controlador.cpython-313.pyc
│     ├─ usuario_controlador.cpython-313.pyc
│     ├─ vehiculo_controlador.cpython-313.pyc
│     ├─ vehiculo_institucional.cpython-313.pyc
│     └─ __init__.cpython-313.pyc
├─ migrations
│  ├─ alembic.ini
│  ├─ env.py
│  ├─ README
│  ├─ script.py.mako
│  ├─ versions
│  │  ├─ 0c5bd98450d7_add_verificado_to_vehiculo.py
│  │  ├─ 3417c381d5bb_add_foto_to_vehiculo.py
│  │  ├─ 6fa35037cbc7_qr_logica.py
│  │  ├─ 6fc3ac4d973a_add_password_to_usuario.py
│  │  ├─ ad4d3584535a_migración_inicial.py
│  │  └─ __pycache__
│  │     ├─ 0c5bd98450d7_add_verificado_to_vehiculo.cpython-313.pyc
│  │     ├─ 3417c381d5bb_add_foto_to_vehiculo.cpython-313.pyc
│  │     ├─ 6fa35037cbc7_qr_logica.cpython-313.pyc
│  │     ├─ 6fc3ac4d973a_add_password_to_usuario.cpython-313.pyc
│  │     └─ ad4d3584535a_migración_inicial.cpython-313.pyc
│  └─ __pycache__
│     └─ env.cpython-313.pyc
├─ models
│  ├─ carga_combustible.py
│  ├─ estacion.py
│  ├─ funcionario_publico.py
│  ├─ persona.py
│  ├─ persona_vehiculo.py
│  ├─ usuario.py
│  ├─ vehiculo.py
│  ├─ vehiculo_institucional.py
│  ├─ __init__.py
│  └─ __pycache__
│     ├─ carga_combustible.cpython-313.pyc
│     ├─ estacion.cpython-313.pyc
│     ├─ funcionario_publico.cpython-313.pyc
│     ├─ persona.cpython-313.pyc
│     ├─ persona_vehiculo.cpython-313.pyc
│     ├─ usuario.cpython-313.pyc
│     ├─ vehiculo.cpython-313.pyc
│     ├─ vehiculo_institucional.cpython-313.pyc
│     └─ __init__.cpython-313.pyc
├─ README.md
├─ requirements.txt
├─ templates
│  ├─ login.html
│  ├─ registrador.html
│  ├─ supervisor.html
│  └─ usuario_qr.html
├─ vercel.json
└─ __pycache__
   └─ app.cpython-313.pyc

```

---

## 🛠️ Pasos de Instalación

### Requisitos previos
- Python
- PostgreSQL
- pgAdmin 4
- Visual Studio Code
- Git (opcional)

---
> [!NOTE]
>Este sistema no esta pensado para funcionar localmente, si bien se puede configurar una base de datos local, las imagenes se guardan en un servicio de Storage, por lo que si se desea que funcione completamente local, se debe adaptar parte del codigo para guardar las imagenes de manera local en una ruta local especifica.

---
### Paso 1
Descargar el Zip desde el repositorio o clonarlo.
![imagen1](docs/imagen1.png)

### Paso 2
Extraer el proyecto y abrirlo con VSCode, en caso de haberlo clonado lo abrimos igualmente con VsCode.
![imagen2](docs/imagen2.png)

### Paso 3
Instalar las librerias necesesarias de los requirements con el comando
```
pip install -r requirements.txt
```
> [!NOTE]
>Se recomienda usar un entorno virtual en caso de tener muchos proyectos con Python para no crear conflictos con las librerias.

### Paso 4
Crear una base de datos con pgAdmin 4 para el proyecto.
![imagen3](docs/imagen3.png)

Le ponemos el nombre que querramos y le damos a save.
![imagen4](docs/imagen4.png)

### Paso 5
Crear el archivo .env en la raiz de la carpeta del proyecto.
![imagen5](docs/imagen5.png)
![imagen6](docs/imagen6.png)

Esto es para crear la variable de entorno que apuntara a la base de datos local, aqui se debe poner lo siguiente, cambiando segun los datos de nuestra base de datos:
```
DATABASE_URL=postgresql://usuario:contraseña@host:puerto/nombre_basedatos
```
Donde dice "usuario" se pone el usuario que al crear una base de datos sin cambiar ningun parametro por defecto es "postgres".
En "contraseña" se pone la contraseña que configuramos al instalar PostgreSQL.
En "host" ponemos localhost ya que es una base de datos local.
En puerto ponemos el puerto que por defecto en bases de datos PostgreSQL es "5432".
Y finalmente en nombre_basedatos ponemos el nombre de la base de datos que previamente creamos.

Nos quedaria algo asi, por ejemplo:
![imagen7](docs/imagen7.png)

### Paso 6
Inicializamos la base de datos ejecutando las migraciones con el comando
```
flask db upgrade
```
![imagen8](docs/imagen8.png)

> [!NOTE]
>Se recomienda en Visual Studio Code usar una terminal cmd en vez de una terminal powershell para ejecutar los comandos.

### Paso 7 
Creamos los usuarios y las estaciones de servicio necesarios en la base de datos para que el proyecto funcione con los siguientes comandos:
```
python add_default_users.py
python add_default_estaciones.py
```
![imagen9](docs/imagen9.png)

### Paso 8
Ejecutamos el proyecto con 
```
flask run
```
![imagen10](docs/imagen10.png)

### Paso 9
Una vez iniciado el servidor local de flask, vamos url que nos proporciona en la terminal manteniendo ctrl y dandole click.
![imagen11](docs/imagen11.png)
![imagen12](docs/imagen12.png)