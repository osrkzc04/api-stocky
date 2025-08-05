# API de Gestión de Bodega - STOCKY

API desarrollada con **FastAPI** y **PostgreSQL**, siguiendo buenas prácticas:
- Arquitectura en capas
- Autenticación con JWT
- Hash de contraseñas con bcrypt
- Conexión a base de datos con Singleton y variables de entorno

## Requisitos previos

- Python 3.10 o superior
- PostgreSQL instalado y en ejecución
- Git instalado
- (Opcional) VS Code para desarrollo

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/osrkzc04/api-stocky
cd nombre-del-proyecto
```

### 2. Crear y activar entorno virtual

#### Windows (PowerShell)
```powershell
python -m venv venv
.
env\Scripts ctivate
```

#### Linux/Mac
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto con la siguiente información:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mi_basedatos
DB_USER=postgres
DB_PASS=123456
SECRET_KEY=supersecreta123
```

## Ejecutar el servidor

### Modo desarrollo (recarga automática)

```bash
uvicorn app.main:app --reload
```

La API estará disponible en:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Comandos útiles

### Exportar dependencias actuales
```bash
pip freeze > requirements.txt
```

### Limpiar cachés de Python
```bash
find . -type d -name "__pycache__" -exec rm -r {} +
```

## Tecnologías utilizadas

- **FastAPI** – Framework web
- **PostgreSQL** – Base de datos relacional
- **SQLAlchemy** – ORM para manejo de modelos
- **Pydantic v2** – Validación de datos
- **Passlib + bcrypt** – Hash de contraseñas
- **JWT (python-jose)** – Autenticación

## Autor

**Oscar Gualoto**
**Fernando Quiguantar**
