# Projet API Ecotrack - backend

Backend réalisé avec `alembic`, `fastapi`

**Penser à dézipper la base de donnée : `backend/projet-api-ecotrack.db`**

## lancement

`cd backend`

1. Configurer le `venv` python et installer les requirements (`pip install -r requirements.txt`)
2. **Vérifier que la BDD est bien présente**. Dézipper ou bien initialiser (avec les instructions ci dessous)
3. Lancer le backend : `uvicorn app.main:app`

Optionnel = pour initialiser la BDD (si elle n'est pas dans le projet)

1. lancer si besoin les migrations alembic (`alembic upgrade head`)
2. lancer l'alimentation des données des villes (`python import_data_0_cities.py`)
3. lancer l'alimentation des données des température (`python import_data_1_temperature.py`)
4. lancer l'alimentation des données air quality (`python import_data_2_air_quality.py`)

Si il y a des limites  d'usage d'API, recommencer a partir de l'id de ville ou ça a échoué.

## alembic pour les migrations

1. `alembic init alembic`
2. Modifier le fichier `alembic/env.py`

```python
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from app.models import Base # that's our Base model

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata # to make the things work

```

3. Renseigner la database

dans le fichier `alembic.ini`

```ini
sqlalchemy.url = sqlite:///projet-api-ecotrack.db
```

4. A chaque modification du modèle

- `alembic revision --autogenerate -m "création de la table movies"`
- `alembic upgrade head`