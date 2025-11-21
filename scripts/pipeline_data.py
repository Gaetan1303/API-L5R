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

# Exemple : transformer la liste en DataFrame pandas
def personnages_to_dataframe(personnages):
    return pd.DataFrame(personnages)

if __name__ == "__main__":
    # Récupération des personnages
    personnages = get_personnages()
    print("Exemple de données :", personnages[:2])
    # Conversion en DataFrame
    df = personnages_to_dataframe(personnages)
    print(df.head())
