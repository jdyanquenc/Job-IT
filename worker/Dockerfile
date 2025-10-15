# ----------------------------
# Etapa base: entorno Python ligero
# ----------------------------
FROM python:3.11-slim

# Define el directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema necesarias para compilar libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia el archivo de requerimientos
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código del worker
COPY . .

# Configuración por defecto
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Comando principal del worker
CMD ["python", "src/worker.py"]
#command: ["watchmedo", "auto-restart", "--patterns=*.py", "--recursive", "python", "src/worker.py"]