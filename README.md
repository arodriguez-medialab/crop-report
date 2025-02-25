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
Si tienes un archivo de respaldo `backup.dump`, usa el siguiente comando:
```bash
pg_restore -U usuario_bd -d nombre_bd -1 backup.dump
```
Si el backup es un `.sql`, usa:
```bash
psql -U usuario_bd -d nombre_bd -f backup.sql
```

### 5️⃣ Configurar las variables de entorno
Renombra `.env.example` a `.env` y edita las variables necesarias.

### 6️⃣ Aplicar migraciones y crear un superusuario
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 7️⃣ Levantar el servidor
```bash
python manage.py runserver
```

🔗 **Accede a la app en:** `http://127.0.0.1:8000/`

---
## 📌 Notas
- Asegúrate de que el servicio de PostgreSQL esté corriendo.
- Recuerda añadir tu `SECRET_KEY` en el archivo `.env`.
- Si hay errores de dependencias, revisa `requirements.txt` y reinstala.

---
📌 **Autor:** Agritop Team 🚀

