from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.dog_service import DogService
from app.services.recommendation_service import recommendation_service
from app.schemas.dog import DogCreate, DogUpdate, DogResponse, BreedCount

router = APIRouter(prefix="/dogs", tags=["Perros"])


@router.get("/breeds/count", response_model=List[BreedCount])
def count_by_breed(db: Session = Depends(get_db)):
    return DogService(db).count_by_breed()


@router.get(
    "/{dog_id}/recommendations",
    summary="Recomendaciones de cuidado por IA",
    response_description="Recomendaciones veterinarias personalizadas generadas por Claude",
)
def get_recommendations(dog_id: int, db: Session = Depends(get_db)):
    dog = DogService(db).get_by_id(dog_id)
    return recommendation_service.get_for_dog(dog)


@router.get("/", response_model=List[DogResponse])
def list_dogs(db: Session = Depends(get_db)):
    return DogService(db).get_all()


@router.get("/{dog_id}", response_model=DogResponse)
def get_dog(dog_id: int, db: Session = Depends(get_db)):
    return DogService(db).get_by_id(dog_id)


@router.post("/", response_model=DogResponse, status_code=status.HTTP_201_CREATED)
def create_dog(data: DogCreate, db: Session = Depends(get_db)):
    return DogService(db).create(data)


@router.put("/{dog_id}", response_model=DogResponse)
def update_dog(dog_id: int, data: DogUpdate, db: Session = Depends(get_db)):
    return DogService(db).update(dog_id, data)


@router.delete("/{dog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dog(dog_id: int, db: Session = Depends(get_db)):
    DogService(db).delete(dog_id)
