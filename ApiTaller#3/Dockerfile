# Utiliza una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requisitos y los instala
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia el resto de los archivos de la aplicación
COPY . .

# Expone el puerto en el que la app correrá
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
