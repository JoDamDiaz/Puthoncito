from typing import Optional
from pydantic import BaseModel, Field
from app.models.dog import Sex


class DogBase(BaseModel):
    name: str = Field(..., max_length=100)
    breed: str = Field(..., max_length=100)
    age: float = Field(..., gt=0)
    weight: float = Field(..., gt=0)
    sex: Sex
    owner: str = Field(..., max_length=150)


class DogCreate(DogBase):
    pass


class DogUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    breed: Optional[str] = Field(None, max_length=100)
    age: Optional[float] = Field(None, gt=0)
    weight: Optional[float] = Field(None, gt=0)
    sex: Optional[Sex] = None
    owner: Optional[str] = Field(None, max_length=150)


class DogResponse(DogBase):
    id: int

    model_config = {"from_attributes": True}


class BreedCount(BaseModel):
    breed: str
    count: int
