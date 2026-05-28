from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.dog_repository import DogRepository
from app.schemas.dog import DogCreate, DogUpdate, DogResponse, BreedCount


class DogService:
    def __init__(self, db: Session):
        self.repo = DogRepository(db)

    def get_all(self) -> List[DogResponse]:
        return self.repo.get_all()

    def get_by_id(self, dog_id: int) -> DogResponse:
        dog = self.repo.get_by_id(dog_id)
        if not dog:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perro no encontrado")
        return dog

    def create(self, data: DogCreate) -> DogResponse:
        return self.repo.create(data)

    def update(self, dog_id: int, data: DogUpdate) -> DogResponse:
        dog = self.repo.get_by_id(dog_id)
        if not dog:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perro no encontrado")
        return self.repo.update(dog, data)

    def delete(self, dog_id: int) -> None:
        dog = self.repo.get_by_id(dog_id)
        if not dog:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perro no encontrado")
        self.repo.delete(dog)

    def count_by_breed(self) -> List[BreedCount]:
        return self.repo.count_by_breed()
