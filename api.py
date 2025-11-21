
from fastapi import FastAPI, HTTPException, Query, Body
from typing import List, Optional, Union
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = FastAPI(title="API L5R Personnages Big Data")

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'dbname': os.getenv('DB_NAME', 'l5r_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASS', 'postgres'),
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

# --- Endpoint GET avec pagination et filtres ---
@app.get("/personnages", summary="Liste paginée et filtrée des personnages")
def get_personnages(
    skip: int = Query(0, ge=0, description="Décalage de pagination (offset)"),
    limit: int = Query(20, ge=1, le=100, description="Nombre max de résultats"),
    clan: Optional[str] = Query(None, description="Filtrer par clan"),
    rang: Optional[int] = Query(None, description="Filtrer par rang")
):
    query = 'SELECT * FROM personnages'
    params = []
    filters = []
    if clan:
        filters.append('clan = %s')
        params.append(clan)
    if rang:
        filters.append('rang = %s')
        params.append(rang)
    if filters:
        query += ' WHERE ' + ' AND '.join(filters)
    query += ' ORDER BY id OFFSET %s LIMIT %s'
    params.extend([skip, limit])
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            return cur.fetchall()

# --- Endpoint GET par ID ---
@app.get("/personnages/{personnage_id}", summary="Récupère un personnage par ID")
def get_personnage(personnage_id: int):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('SELECT * FROM personnages WHERE id = %s;', (personnage_id,))
            perso = cur.fetchone()
            if not perso:
                raise HTTPException(status_code=404, detail="Personnage non trouvé")
            return perso

# --- Endpoint d'analyse : nombre de personnages par clan ---
@app.get("/stats/personnages/clans", summary="Nombre de personnages par clan")
def stats_personnages_par_clan():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('SELECT clan, COUNT(*) as count FROM personnages GROUP BY clan ORDER BY count DESC;')
            return cur.fetchall()

# --- Endpoint POST pour insertion unitaire ou en masse ---
@app.post("/personnages", summary="Ajoute un ou plusieurs personnages")
def add_personnages(payload: Union[dict, List[dict]] = Body(...)):
    """
    Ajoute un ou plusieurs personnages. Le payload peut être un objet ou une liste d'objets.
    Chaque personnage doit contenir au minimum : nom, clan, rang, data (dict ou JSON).
    """
    if isinstance(payload, dict):
        personnages = [payload]
    else:
        personnages = payload
    inserted = []
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            for perso in personnages:
                nom = perso.get('nom')
                clan = perso.get('clan')
                rang = perso.get('rang')
                data = perso.get('data', {})
                if not (nom and clan and rang is not None):
                    continue  # Ignore les entrées incomplètes
                cur.execute(
                    'INSERT INTO personnages (nom, clan, rang, data) VALUES (%s, %s, %s, %s) RETURNING *;',
                    (nom, clan, rang, data)
                )
                inserted.append(cur.fetchone())
            conn.commit()
    return {"inserted": inserted, "count": len(inserted)}

# Pour lancer : source .venv/bin/activate && uvicorn api:app --reload
