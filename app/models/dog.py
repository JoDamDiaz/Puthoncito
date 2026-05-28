from sqlalchemy import Column, Integer, String, Float, Date, Enum
from app.database import Base
import enum


class Sex(str, enum.Enum):
    macho = "macho"
    hembra = "hembra"


class Dog(Base):
    __tablename__ = "dogs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    breed = Column(String(100), nullable=False)
    age = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    sex = Column(Enum(Sex), nullable=False)
    owner = Column(String(150), nullable=False)
