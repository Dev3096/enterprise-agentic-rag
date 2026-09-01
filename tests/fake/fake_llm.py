from enterprise_rag.llm.base import LLMProvider


class FakeLLMProvider(LLMProvider):
    def __init__(self, response: str) -> None:
        self.response = response
        self.last_system_prompt: str | None = None
        self.last_user_prompt: str | None = None

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        self.last_system_prompt = system_prompt
        self.last_user_prompt = user_prompt

        return self.response