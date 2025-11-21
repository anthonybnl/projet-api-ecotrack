import os
import pandas as pd
from app import models, database

df_base_codes_postaux = pd.read_csv(
    os.path.join(os.getcwd(), "data", "base-officielle-codes-postaux.csv")
)

# nettoyage de données

df_base_codes_postaux = df_base_codes_postaux[
    ["code_commune_insee", "nom_de_la_commune", "code_postal", "latitude", "longitude"]
]

df_base_codes_postaux = df_base_codes_postaux.drop_duplicates()

df_base_codes_postaux = df_base_codes_postaux[df_base_codes_postaux["latitude"].notna()]

# croisement pour ne garder que les grandes villes

df_grandes_villes = pd.read_csv(
    os.path.join(os.getcwd(), "data", "grande_ville_france.csv")
)

df_base_codes_postaux = df_base_codes_postaux.merge(
    right=df_grandes_villes,
    how="inner",
    left_on="code_commune_insee",
    right_on="code_insee",
)


# doublon de code_insee ou code_postal

df_base_codes_postaux = df_base_codes_postaux.drop_duplicates(
    "code_postal", keep="first"
)
df_base_codes_postaux = df_base_codes_postaux.drop_duplicates(
    "code_commune_insee", keep="first"
)

# insertion

cities = []

for row in df_base_codes_postaux.itertuples():

    departement = int(str(row.code_postal)[0:2])

    city = models.City(
        code_insee=row.code_commune_insee,
        name=row.nom_de_la_commune,
        code_postal=row.code_postal,
        departement=departement,
        lat=round(row.latitude, 6),
        lng=round(row.longitude, 6),
    )
    cities.append(city)

print(f"intégration des {len(cities)} villes ...")

with database.Sessionmaker() as session:
    session.add_all(cities)
    session.commit()
