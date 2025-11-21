from sqlalchemy.orm import Session
from app.models import City
from app.database import Sessionmaker


def get_all_cities(session: Session):
    results = session.query(City)
    return results.all()


def get_city_by_id(session: Session, id: int):
    result = session.get(City, id)
    return result


def get_city_by_code_insee(session: Session, code_insee: str):
    results = session.query(City).filter(City.code_insee == code_insee).all()
    if len(results) == 0:
        return None
    return results[0]


def get_city_by_code_postal(session: Session, code_postal: int):
    results = session.query(City).filter(City.code_postal == code_postal).all()
    if len(results) == 0:
        return None
    return results[0]


def create_city(session: Session, city: City):
    try:
        city_db = City(
            code_insee=city.code_insee,
            name=city.name,
            code_postal=city.code_postal,
            departement=city.departement,
            lat=city.lat,
            lng=city.lng,
        )
        session.add(city_db)
        session.commit()
        session.refresh(city_db)
        return city_db
    except Exception:
        session.rollback()
        raise


def update_city(session: Session, id: int, city: City):
    try:
        city_db = session.get(City, id)
        if city_db is None:
            return None

        if city.code_insee is not None:
            city_db.code_insee = city.code_insee

        if city.name is not None:
            city_db.name = city.name

        if city.code_postal is not None:
            city_db.code_postal = city.code_postal

        if city.departement is not None:
            city_db.departement = city.departement

        if city.lat is not None:
            city_db.lat = city.lat

        if city.lng is not None:
            city_db.lng = city.lng

        session.add(city_db)
        session.commit()
        session.refresh(city_db)

        return city_db
    except Exception:
        session.rollback()
        raise


def delete_city(session: Session, id: int):
    try:
        db_city = session.get(City, id)
        if db_city is None:
            return None
        session.delete(db_city)
        session.commit()
        return db_city
    except Exception as e:
        raise
