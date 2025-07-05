# ms-gestion-poliza/Dockerfile
FROM python:3.11-slim

LABEL maintainer="Pacífico Health Insurance Team"
LABEL description="MS Gestión Poliza - Microservicio para gestión de pólizas"

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de dependencias
COPY requirements.txt* ./

# Crear requirements.txt si no existe
RUN if [ ! -f requirements.txt ]; then \
    echo "fastapi==0.104.1" > requirements.txt && \
    echo "uvicorn[standard]==0.24.0" >> requirements.txt && \
    echo "pydantic==2.5.0" >> requirements.txt && \
    echo "mysql-connector-python==8.2.0" >> requirements.txt; \
    fi

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Crear usuario no-root
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Exponer puerto
EXPOSE 8002

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8002/ || exit 1

# Comando por defecto
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]
