from sentence_transformers import SentenceTransformer

from enterprise_rag.embeddings.base import EmbeddingProvider


class SentenceTransformerEmbeddingProvider(EmbeddingProvider):

    def __init__(
        self,
        model_name: str = "BAAI/bge-small-en-v1.5",
    ) -> None:
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> list[float]:
        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def embed_texts(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
        )

        return embeddings.tolist()