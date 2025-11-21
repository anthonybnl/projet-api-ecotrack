from sqlalchemy import (
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    String,
    Float,
    UniqueConstraint,
    DateTime,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code_insee = Column(String, nullable=False)
    name = Column(String, nullable=False)
    code_postal = Column(Integer, nullable=False)
    departement = Column(Integer, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)

    measurements = relationship("Measurement", back_populates="city")

    __table_args__ = (
        UniqueConstraint("code_insee", name="uq_cities_code_insee"),
        UniqueConstraint("code_postal", name="uq_cities_code_postal"),
    )

    def __repr__(self):
        return f'City(id={self.id}, name="{self.name}")'


class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String, nullable=False)
    type = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    datetime = Column(DateTime, nullable=False)

    # Clé étrangère vers City
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    city = relationship("City", back_populates="measurements")

    __table_args__ = (
        UniqueConstraint(
            "type", "datetime", "city_id", name="uq_measurements_type_datetime_city"
        ),
    )

    def __repr__(self):
        return f"Measurement(id={self.id}, type='{self.type}', date={self.date}, value={self.value})"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("email", name="uq_users_email"),
        CheckConstraint(
            "role in ('user', 'admin')",
            name="ck_users_role",
        ),
    )

    def __repr__(self):
        return f'User(id={self.id}, email="{self.email}")'
