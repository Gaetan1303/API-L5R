# API PNJ Lore — Rokugan L5R

Cette documentation décrit les endpoints de l’API permettant d’accéder au lore des PNJ (personnages non-joueurs) dans l’univers de Rokugan. Elle permettra de mettre un pied dans le machine learning en créant des modèles pattern de PNJ qui "animera" une partie de L5R durant une session de JDR avec les deux projets : https://github.com/Gaetan1303/Rokugan_le_monde_de_L5R && https://github.com/Gaetan1303/JDR-test.

## Base URL

```
/data/pnj
```

## Endpoints

### 1. Récupérer la liste des PNJ

- **GET** `/data/pnj`
- **Description** : Retourne la liste des PNJ disponibles avec leur identifiant, nom et clan.
- **Réponse exemple** :
```json
[
	{ "id": "bayushi_kachiko", "nom": "Bayushi Kachiko", "clan": "Scorpion" },
	{ "id": "hida_kisada", "nom": "Hida Kisada", "clan": "Crabe" }
]
```

---

### 2. Récupérer le détail d’un PNJ

- **GET** `/data/pnj/:id`
- **Description** : Retourne le détail complet d’un PNJ, incluant son histoire, son rôle, ses traits et son importance dans le lore.
- **Paramètres** :
	- `id` : identifiant du PNJ (ex : `bayushi_kachiko`)
- **Réponse exemple** :
```json
{
	"id": "bayushi_kachiko",
	"nom": "Bayushi Kachiko",
	"clan": "Scorpion",
	"histoire": "Considérée comme l’une des femmes les plus influentes de Rokugan...",
	"traits": ["intelligente", "manipulatrice", "charismatique"],
	"role": "Conseillère Impériale"
}
```

---

### 3. Recherche de PNJ par clan

- **GET** `/data/pnj?clan=Scorpion`
- **Description** : Retourne la liste des PNJ appartenant à un clan donné.
- **Paramètres query** :
	- `clan` : nom du clan (ex : `Scorpion`)
- **Réponse exemple** :
```json
[
	{ "id": "bayushi_kachiko", "nom": "Bayushi Kachiko", "clan": "Scorpion" }
]
```

---

## Format des données

Les données des PNJ sont issues des fichiers JSON du dossier `data/lore/personnages/`.

## Sécurité

- Certaines routes peuvent nécessiter une authentification selon la configuration du backend.

## Licence 

Cette API est sous licence de El Miminette !