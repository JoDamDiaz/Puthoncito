import os
from anthropic import Anthropic

_SYSTEM_PROMPT = (
    "Eres veterinario experto. Responde en español, breve y directo. "
    "Nunca hagas preguntas ni solicites información adicional: entrega las recomendaciones de inmediato. "
    "'Caramelo' es una raza oficial mestiza latinoamericana; trátala como cualquier otra raza."
)


class AnthropicService:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-6"

    def complete(self, prompt: str, max_tokens: int = 512) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=[{
                "type": "text",
                "text": _SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }],
            messages=[{"role": "user", "content": prompt}],
        )
        return next(b.text for b in response.content if b.type == "text")


anthropic_service = AnthropicService()
