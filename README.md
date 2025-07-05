# MS Gestión Póliza

API REST para gestión de pólizas y productos de seguros desarrollada con FastAPI.

## 🚀 Ejecución con Docker

### Opción 1: Docker Compose (Recomendado)

Para ejecutar la aplicación completa con MySQL:

```bash
# Construir y ejecutar todos los servicios
docker-compose up --build

# Ejecutar en segundo plano
docker-compose up -d --build

# Detener los servicios
docker-compose down
```

### Opción 2: Docker individual

```bash
# Construir la imagen
docker build -t ms-gestion-poliza .

# Ejecutar el contenedor
docker run -p 8000:8000 --name ms-gestion-poliza-api ms-gestion-poliza
```

## 📋 Endpoints disponibles

### Health Check
- `GET /health` - Verificación de salud del servicio

### Productos
- `GET /productos` - Obtener todos los productos de seguros
- `GET /producto/{codigo}` - Obtener un producto específico por código

### Pólizas
- `GET /polizas/{codigo_persona}` - Obtener pólizas por código de persona

## 📖 Documentación

Una vez ejecutada la aplicación, puedes acceder a:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🗄️ Base de Datos

La aplicación utiliza MySQL con las siguientes credenciales por defecto:
- **Host**: localhost (o mysql en Docker Compose)
- **Puerto**: 3306
- **Usuario**: root
- **Contraseña**: root
- **Base de datos**: db_poliza

## 🔧 Variables de Entorno

Puedes configurar la conexión a la base de datos usando estas variables de entorno:

```bash
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DATABASE=db_poliza
```