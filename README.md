# Proyecto Django con PostgreSQL

Este repositorio contiene un proyecto desarrollado con **Django** y usa **PostgreSQL** como base de datos.

## 🚀 Instalación y configuración

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/arodriguez-medialab/crop-report.git
cd crop-report
```

### 2️⃣ Crear un entorno virtual y activarlo
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar la base de datos
Este proyecto usa **PostgreSQL**, asegúrate de tenerlo instalado y configurado.

#### 🔹 Crear la base de datos y usuario en PostgreSQL
```sql
CREATE DATABASE nombre_bd;
CREATE USER usuario_bd WITH PASSWORD 'tu_contraseña';
ALTER ROLE usuario_bd SET client_encoding TO 'utf8';
ALTER ROLE usuario_bd SET default_transaction_isolation TO 'read committed';
ALTER ROLE usuario_bd SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE nombre_bd TO usuario_bd;
```

#### 🔹 Restaurar la base de datos desde un backup (`.dump` o `.sql`)
Si tienes un archivo de respaldo `backup_agritop_bd_240225.dump`, usa el siguiente comando:
```bash
pg_restore -U usuario_bd -d nombre_bd -1 backup_agritop_bd_240225.dump
```
Si el backup es un `.sql`, usa:
```bash
psql -U usuario_bd -d nombre_bd -f backup.sql
```

### 5️⃣ Configurar las variables de entorno
Renombra `.env.example` a `.env` y edita las variables necesarias.
```

### 6️⃣ Aplicar migraciones y crear un superusuario
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 7️⃣ Levantar el servidor en desarrollo
```bash
python manage.py runserver
```
🔗 **Accede a la app en:** `http://127.0.0.1:8000/`

---
## 🔧 Configuración para producción
Para ejecutar este proyecto en un entorno de producción, usa el siguiente script de arranque:

```sh
#!/bin/sh

echo $APP_PATH
path_project=$APP_PATH

echo 'export APP_PATH='$path_project >> ~/.bashrc
echo 'cd $APP_PATH' >> ~/.bashrc

# Entrar en el directorio del proyecto
cd $path_project

export APP_PATH=$path_project
if [ -z "$HOST" ]; then
        export HOST=0.0.0.0
fi

if [ -z "$PORT" ]; then
        export PORT=80
fi

export PATH="/opt/python/3.9.7/bin:${PATH}"
echo 'export VIRTUALENVIRONMENT_PATH='$path_project'antenv' >> ~/.bashrc
echo '. antenv/bin/activate' >> ~/.bashrc
PYTHON_VERSION=$(python -c "import sys; print(str(sys.version_info.major) + '.' + str(sys.version_info.minor))")
echo Usando paquetes del entorno virtual 'antenv' en $path_project'/antenv'.
export PYTHONPATH=$PYTHONPATH:$path_project"/antenv/lib/python$PYTHON_VERSION/site-packages"
echo "PYTHONPATH actualizado a '$PYTHONPATH'"
. antenv/bin/activate
nohup python $path_project/manage.py process_tasks &
# Ejecutando tareas en segundo plano
GUNICORN_CMD_ARGS="--timeout 600 --access-logfile '-' --error-logfile '-' -c /opt/startup/gunicorn.conf.py --chdir="$path_project gunicorn agritop_backend.wsgi
```

---
📌 **Autor:** Agritop Team 🚀

