import requests
from datetime import datetime

from app.database import Sessionmaker
from app import models

url = "https://air-quality-api.open-meteo.com/v1/air-quality"


def get_data_for_this_lat_lng(lat: float, lng: float):

    params = {
        "latitude": lat,
        "longitude": lng,
        "hourly": "pm2_5",
        "past_days":92,
        "forecast_days":1
    }

    response = requests.get(url, params=params)
    response.raise_for_status()  # génère une erreur si la requête échoue

    data = response.json()

    datetimes = data["hourly"]["time"]
    pm25s = data["hourly"]["pm2_5"]

    results = []
    for i in range(len(datetimes)):
        dt = datetimes[i]
        pm25 = pm25s[i]

        results.append(
            (
                dt,
                pm25,
            )
        )
    return results


# with Sessionmaker() as session:
#     old = session.query(models.Measurement).filter(models.Measurement.type == "Particulate Matter PM2_5").all()

#     print(f"suppression de {len(old)} anciennes données")
#     for measurement in old:
#         session.delete(measurement)
#     session.commit()

with Sessionmaker() as session:
    # res = session.query(models.City).all()
    res = (
        session.query(models.City).filter(models.City.id >= 228).all()
    )  # obligé de le faire en plusieurs fois, limite d'API

    nb_cities = len(res)
    for i, city in enumerate(res):
        print(
            f"récupération des données air quality de la ville : {city.name} - {i+1} / {nb_cities}"
        )
        data = get_data_for_this_lat_lng(city.lat, city.lng)

        measurements = []

        for dt_str, pm2_5 in data:

            dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M")

            measurement = models.Measurement(
                source="https://air-quality-api.open-meteo.com/v1/air-quality",
                type="Particulate Matter PM2_5",
                value=pm2_5,
                unit="μg/m³",
                datetime=dt,
                city=city,
            )

            measurements.append(measurement)

        session.add_all(measurements)
        session.commit()
