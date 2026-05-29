from app.models.cat import Cat
from app.services.anthropic_service import AnthropicService, anthropic_service


class CatRecommendationService:
    def __init__(self, service: AnthropicService = anthropic_service):
        self.anthropic = service

    def _build_prompt(self, cat: Cat) -> str:
        return (
            f"Gato: {cat.breed}, {cat.age}a, {cat.weight}kg, {cat.sex.value}\n"
            f"Recomienda brevemente: 1.Alimentación 2.Ejercicio/enriquecimiento 3.Salud preventiva 4.Aseo 5.Raza"
        )

    def get_for_cat(self, cat: Cat) -> dict:
        prompt = self._build_prompt(cat)
        recommendations = self.anthropic.complete(prompt)
        return {
            "cat_id": cat.id,
            "cat_name": cat.name,
            "breed": cat.breed,
            "recommendations": recommendations,
        }


cat_recommendation_service = CatRecommendationService()
