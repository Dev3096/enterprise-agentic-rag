from openai import OpenAI

from enterprise_rag.config.settings import get_settings
from enterprise_rag.llm.base import LLMProvider


class OpenAILLMProvider(LLMProvider):
    def __init__(self) -> None:
        settings = get_settings()

        if not settings.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY must be configured to use OpenAILLMProvider"
            )

        self.model = settings.openai_model

        self.client = OpenAI(
            api_key=settings.openai_api_key,
        )

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        response = self.client.responses.create(
            model=self.model,
            instructions=system_prompt,
            input=user_prompt,
        )

        return response.output_text