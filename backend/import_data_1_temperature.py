import requests
from datetime import datetime
from app.database import Sessionmaker
from app import models

url = "https://archive-api.open-meteo.com/v1/archive"


def get_data_for_this_lat_lng(lat: float, lng: float):
    now = datetime.now().strftime("%Y-%m-%d")

    params = {
        "latitude": lat,
        "longitude": lng,
        "start_date": "2024-01-01",
        "end_date": now,
        "daily": "temperature_2m_mean",
        "timezone": "UTC",
    }

    response = requests.get(url, params=params)
    response.raise_for_status()  # génère une erreur si la requête échoue

    data = response.json()

    dates = data["daily"]["time"]
    temperatures = data["daily"]["temperature_2m_mean"]

    results = []
    for i in range(len(dates)):
        date = dates[i]
        temperature = temperatures[i]

        results.append(
            (
                date,
                temperature,
            )
        )
    return results

with Sessionmaker() as session:
    # res = session.query(models.City).all()
    # res = (
    #     session.query(models.City).filter(models.City.id >= 196).all()
    # )  # obligé de le faire en plusieurs fois, limite d'API
    res = (
        session.query(models.City).filter(models.City.id < 196).all()
    )  # obligé de le faire en plusieurs fois, limite d'API

    nb_cities = len(res)
    for i, city in enumerate(res):
        print(
            f"récupération des données de la ville : {city.name} - {i+1} / {nb_cities}"
        )
        data = get_data_for_this_lat_lng(city.lat, city.lng)

        measurements = []

        for date, temperature in data:
            date = datetime.strptime(date, "%Y-%m-%d").date()
            dt = datetime(date.year, date.month, date.day)

            measurement = models.Measurement(
                source="https://archive-api.open-meteo.com/v1/archive",
                type="temperature",
                value=temperature,
                unit="°C",
                datetime=dt,
                city=city,
            )

            measurements.append(measurement)

        session.add_all(measurements)
        session.commit()
