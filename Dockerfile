# Imagen base ligera
FROM python:3.11-slim

# Buenas prácticas: no correr como root
RUN useradd --create-home appuser

# Directorio de trabajo
WORKDIR /app

# Copiar dependencias primero (aprovecha caché de Docker)
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Cambiar al usuario sin privilegios
USER appuser

# Puerto que expone Flask
EXPOSE 5000

# Comando de arranque
CMD ["python", "main.py"]