from sqlalchemy.orm import Session
from app.models import Measurement, City
from app.database import Sessionmaker
from datetime import datetime
from sqlalchemy.orm import Query, selectinload


def apply_filter(
    results: Query[Measurement],
    date_start: datetime = None,
    date_end: datetime = None,
    departement: int = None,
    type: str = None,
):
    # filtre dates

    if date_start is not None:
        results = results.filter(Measurement.datetime >= date_start)

    if date_end is not None:
        results = results.filter(Measurement.datetime < date_end)

    # filtre departement (zone)

    if departement is not None:
        results = results.join(Measurement.city).filter(City.departement == departement)

    # filtre type : "temperature" ou "Particulate Matter PM2_5"

    if type is not None:
        results = results.filter(Measurement.type == type)

    return results


def get_all_measurements(
    session: Session,
    date_start: datetime = None,
    date_end: datetime = None,
    departement: int = None,
    type: str = None,
    limit: int = 500,
    offset: int = 0,
):
    results = session.query(Measurement)

    results = apply_filter(results, date_start, date_end, departement, type)

    results = results.limit(limit).offset(offset)
    return results.all()


def get_all_measurements_include_city(
    session: Session,
    date_start: datetime = None,
    date_end: datetime = None,
    departement: int = None,
    type: str = None,
):
    results = session.query(Measurement)
    results = results.options(selectinload(Measurement.city))

    results = apply_filter(results, date_start, date_end, departement, type)

    return results.all()


def get_mesurement_by_id(session: Session, id: int):
    result = session.get(Measurement, id)
    return result


def create_measurement(session: Session, measurement: Measurement, city: City):
    try:
        measurement_db = Measurement(
            source=measurement.source,
            type=measurement.type,
            value=measurement.value,
            unit=measurement.unit,
            datetime=measurement.datetime,
            city=city,
        )
        session.add(measurement_db)
        session.commit()
        session.refresh(measurement_db)
        return measurement_db
    except Exception:
        session.rollback()
        raise


def update_measurement(session: Session, id: int, measurement: Measurement):
    try:
        measurement_db = session.get(Measurement, id)
        if measurement_db is None:
            return None

        if measurement.source is not None:
            measurement_db.source = measurement.source

        if measurement.type is not None:
            measurement_db.type = measurement.type

        if measurement.value is not None:
            measurement_db.value = measurement.value

        if measurement.unit is not None:
            measurement_db.unit = measurement.unit

        if measurement.datetime is not None:
            measurement_db.datetime = measurement.datetime

        if measurement.city_id is not None:
            measurement_db.city_id = measurement.city_id

        session.add(measurement_db)
        session.commit()
        session.refresh(measurement_db)

        return measurement_db
    except Exception:
        session.rollback()
        raise


def delete_measurement(session: Session, id: int):
    try:
        measurement_db = session.get(Measurement, id)
        if measurement_db is None:
            return None
        session.delete(measurement_db)
        session.commit()
        return measurement_db
    except Exception as e:
        raise
