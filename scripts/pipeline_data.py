# --- Tables PNJ et Dialogue ---
def create_pnj_table():
    query = '''
        CREATE TABLE IF NOT EXISTS pnjs (
            id SERIAL PRIMARY KEY,
            nom VARCHAR(100),
            clan VARCHAR(50),
            role VARCHAR(100),
            personnalite TEXT,
            connaissances_lore TEXT[],
            description TEXT
        );
    '''
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()

def create_dialogue_table():
    query = '''
        CREATE TABLE IF NOT EXISTS dialogues (
            id SERIAL PRIMARY KEY,
            pnj_id INTEGER REFERENCES pnjs(id) ON DELETE CASCADE,
            theme VARCHAR(100),
            titre VARCHAR(200),
            repliques JSONB
        );
    '''
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()

# --- Création des tables si besoin ---
if __name__ == "__main__":
    create_personnages_table()
    create_pnj_table()
    create_dialogue_table()

import psycopg2
from psycopg2.extras import RealDictCursor
import os

# --- Configuration de la base PostgreSQL ---
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'dbname': os.getenv('DB_NAME', 'l5r_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASS', 'postgres'),
}

def get_connection():
    """Crée une connexion à la base PostgreSQL."""
    return psycopg2.connect(**DB_CONFIG)

# --- Fonctions de gestion des personnages ---
def create_personnages_table():
    """Crée la table personnages si elle n'existe pas."""
    query = '''
        CREATE TABLE IF NOT EXISTS personnages (
            id SERIAL PRIMARY KEY,
            nom VARCHAR(100),
            clan VARCHAR(50),
            rang INT,
            data JSONB
        );
    '''
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()

def get_all_personnages():
    """Récupère tous les personnages."""
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('SELECT * FROM personnages;')
            return cur.fetchall()

def get_personnage_by_id(personnage_id):
    """Récupère un personnage par son ID."""
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('SELECT * FROM personnages WHERE id = %s;', (personnage_id,))
            return cur.fetchone()

# --- Exemple d'utilisation en script ---
if __name__ == "__main__":
    create_personnages_table()
    print("Tous les personnages :")
    for perso in get_all_personnages():
        print(perso)
    print("\nPersonnage avec id=1 :")
    print(get_personnage_by_id(1))
import requests
import pandas as pd

# URL de base de ton backend
BASE_URL = "https://gm-l5r.onrender.com"

# Exemple : récupérer la liste des personnages (adapter selon la route réelle)
def get_personnages():
    url = f"{BASE_URL}/api/pnj"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    # Récupération des personnages
    personnages = get_personnages()
    print("Exemple de données :", personnages[:2])
    # Conversion en DataFrame
    df = personnages_to_dataframe(personnages)
    print(df.head())
