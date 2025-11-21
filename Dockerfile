# Utilise une image Python officielle
FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt ./

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code
COPY . .

# Exposer le port utilisé par Flask-SocketIO
EXPOSE 5000

# Lancer le serveur avec eventlet
CMD ["python", "server.py"]
