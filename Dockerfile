FROM python:3.11-slim-buster

# ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libffi-dev libssl-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /requirements.txt

# Instalar las dependencias del bot
RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copiar el código del bot al contenedor
COPY ./app/ /app
WORKDIR /app

# Ejecutar el bot cuando se inicie el contenedor
# CMD ["python", "main.py"]
CMD ["uvicorn", "app.main:rpi_mon_api", "--host", "0.0.0.0", "--port", "80"]