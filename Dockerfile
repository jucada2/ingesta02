# Imagen base
FROM python:3.10-slim

# Instala dependencias del sistema necesarias para mysqlclient
RUN apt-get update && apt-get install -y gcc default-libmysqlclient-dev

# Crear directorio de trabajo
WORKDIR /app

# Copiar los archivos necesarios
COPY ingesta.py .
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando por defecto al ejecutar el contenedor
CMD ["python", "ingesta2.py"]