from enterprise_rag.rag.service import RAGService
from functools import lru_cache
from enterprise_rag.embeddings.sentence_transformer import SentenceTransformerEmbeddingProvider
from enterprise_rag.retrieval.vector_search import VectorSearchRepository
from enterprise_rag.reranking.cross_encoder import CrossEncoderReranker
from enterprise_rag.retrieval.service import RetrievalService

@lru_cache(maxsize=1)
def get_rag_service() -> RAGService:
    embedding_provider = SentenceTransformerEmbeddingProvider()
    vector_search = VectorSearchRepository()
    reranker = CrossEncoderReranker()
    retrieval = RetrievalService(embedding_provider= embedding_provider, search_repository= vector_search, reranker= reranker)
    raise NotImplementedError