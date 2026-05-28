from typing import Optional, List
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.cat import Cat
from app.schemas.cat import CatCreate, CatUpdate, BreedCount


class CatRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Cat]:
        return self.db.query(Cat).all()

    def get_by_id(self, cat_id: int) -> Optional[Cat]:
        return self.db.query(Cat).filter(Cat.id == cat_id).first()

    def create(self, data: CatCreate) -> Cat:
        cat = Cat(**data.model_dump())
        self.db.add(cat)
        self.db.commit()
        self.db.refresh(cat)
        return cat

    def update(self, cat: Cat, data: CatUpdate) -> Cat:
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(cat, field, value)
        self.db.commit()
        self.db.refresh(cat)
        return cat

    def delete(self, cat: Cat) -> None:
        self.db.delete(cat)
        self.db.commit()

    def count_by_breed(self) -> List[BreedCount]:
        rows = (
            self.db.query(Cat.breed, func.count(Cat.id).label("count"))
            .group_by(Cat.breed)
            .order_by(func.count(Cat.id).desc())
            .all()
        )
        return [BreedCount(breed=breed, count=count) for breed, count in rows]
