# Utiliza una imagen base con Python y sistema operativo (alpine es una opción ligera)
FROM python:2.7-alpine

RUN apk update

# Instala las dependencias necesarias para compilar Pillow
RUN apk add build-base python-dev jpeg-dev zlib-dev

# Instala las dependencias necesarias para conectar con mysql
RUN apk add mysql-dev

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala las dependencias de la aplicación
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia los archivos del proyecto
COPY . /app/

# Hacer collectstatic
RUN python manage.py collectstatic --noinput

# Expone el puerto 8000 para acceder a la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
