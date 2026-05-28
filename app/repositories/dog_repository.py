from typing import Optional, List
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.dog import Dog
from app.schemas.dog import DogCreate, DogUpdate, BreedCount


class DogRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Dog]:
        return self.db.query(Dog).all()

    def get_by_id(self, dog_id: int) -> Optional[Dog]:
        return self.db.query(Dog).filter(Dog.id == dog_id).first()

    def create(self, data: DogCreate) -> Dog:
        dog = Dog(**data.model_dump())
        self.db.add(dog)
        self.db.commit()
        self.db.refresh(dog)
        return dog

    def update(self, dog: Dog, data: DogUpdate) -> Dog:
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(dog, field, value)
        self.db.commit()
        self.db.refresh(dog)
        return dog

    def delete(self, dog: Dog) -> None:
        self.db.delete(dog)
        self.db.commit()

    def count_by_breed(self) -> List[BreedCount]:
        rows = (
            self.db.query(Dog.breed, func.count(Dog.id).label("count"))
            .group_by(Dog.breed)
            .order_by(func.count(Dog.id).desc())
            .all()
        )
        return [BreedCount(breed=breed, count=count) for breed, count in rows]
