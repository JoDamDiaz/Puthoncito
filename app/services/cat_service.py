from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.cat_repository import CatRepository
from app.schemas.cat import CatCreate, CatUpdate, CatResponse, BreedCount


class CatService:
    def __init__(self, db: Session):
        self.repo = CatRepository(db)

    def get_all(self) -> List[CatResponse]:
        return self.repo.get_all()

    def get_by_id(self, cat_id: int) -> CatResponse:
        cat = self.repo.get_by_id(cat_id)
        if not cat:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gato no encontrado")
        return cat

    def create(self, data: CatCreate) -> CatResponse:
        return self.repo.create(data)

    def update(self, cat_id: int, data: CatUpdate) -> CatResponse:
        cat = self.repo.get_by_id(cat_id)
        if not cat:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gato no encontrado")
        return self.repo.update(cat, data)

    def delete(self, cat_id: int) -> None:
        cat = self.repo.get_by_id(cat_id)
        if not cat:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gato no encontrado")
        self.repo.delete(cat)

    def count_by_breed(self) -> List[BreedCount]:
        return self.repo.count_by_breed()
