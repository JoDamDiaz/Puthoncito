from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.cat_service import CatService
from app.services.cat_recommendation_service import cat_recommendation_service
from app.schemas.cat import CatCreate, CatUpdate, CatResponse, BreedCount

router = APIRouter(prefix="/cats", tags=["Gatos"])


@router.get("/breeds/count", response_model=List[BreedCount])
def count_by_breed(db: Session = Depends(get_db)):
    return CatService(db).count_by_breed()


@router.get(
    "/{cat_id}/recommendations",
    summary="Recomendaciones de cuidado por IA",
    response_description="Recomendaciones veterinarias personalizadas generadas por Claude",
)
def get_recommendations(cat_id: int, db: Session = Depends(get_db)):
    cat = CatService(db).get_by_id(cat_id)
    return cat_recommendation_service.get_for_cat(cat)


@router.get("/", response_model=List[CatResponse])
def list_cats(db: Session = Depends(get_db)):
    return CatService(db).get_all()


@router.get("/{cat_id}", response_model=CatResponse)
def get_cat(cat_id: int, db: Session = Depends(get_db)):
    return CatService(db).get_by_id(cat_id)


@router.post("/", response_model=CatResponse, status_code=status.HTTP_201_CREATED)
def create_cat(data: CatCreate, db: Session = Depends(get_db)):
    return CatService(db).create(data)


@router.put("/{cat_id}", response_model=CatResponse)
def update_cat(cat_id: int, data: CatUpdate, db: Session = Depends(get_db)):
    return CatService(db).update(cat_id, data)


@router.delete("/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cat(cat_id: int, db: Session = Depends(get_db)):
    CatService(db).delete(cat_id)
