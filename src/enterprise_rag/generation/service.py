from enterprise_rag.llm.base import LLMProvider
from enterprise_rag.retrieval.vector_search import SearchResult


class GenerationService:
    def __init__(
        self,
        llm_provider: LLMProvider,
    ) -> None:
        self.llm_provider = llm_provider

    def generate_answer(
        self,
        question: str,
        results: list[SearchResult],
    ) -> str:
        if not results:
            return "I do not have enough information to answer this question."

        system_prompt = (
            "You are an enterprise support assistant. "
            "Answer only using the provided evidence. "
            "If the evidence is insufficient, say that you do not have "
            "enough information to answer. "
            "Do not invent facts. "
            "When making factual claims, cite the supporting evidence using "
            "the evidence number in square brackets, for example [1] or [2]. "
            "Only use citation numbers that appear in the provided evidence."
        )
        context_blocks: list[str] = []

        for index, result in enumerate(results, start=1):
            section = result.heading or "Unknown section"

            context_blocks.append(
                f"[{index}] {result.title} > {section}\n"
                f"{result.content}"
            )

        context = "\n\n".join(context_blocks)

        user_prompt = (
            f"Question:\n{question}\n\n"
            f"Evidence:\n{context}"
        )

        return self.llm_provider.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )