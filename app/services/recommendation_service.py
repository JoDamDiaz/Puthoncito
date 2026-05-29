from app.models.dog import Dog
from app.services.anthropic_service import AnthropicService, anthropic_service


class RecommendationService:
    def __init__(self, service: AnthropicService = anthropic_service):
        self.anthropic = service

    def _build_prompt(self, dog: Dog) -> str:
        return (
            f"Perro: {dog.breed}, {dog.age}a, {dog.weight}kg, {dog.sex.value}\n"
            f"Recomienda brevemente: 1.Alimentación 2.Ejercicio 3.Salud preventiva 4.Aseo 5.Raza"
        )

    def get_for_dog(self, dog: Dog) -> dict:
        prompt = self._build_prompt(dog)
        recommendations = self.anthropic.complete(prompt)
        return {
            "dog_id": dog.id,
            "dog_name": dog.name,
            "breed": dog.breed,
            "recommendations": recommendations,
        }


recommendation_service = RecommendationService()
