import json
from pathlib import Path

from enterprise_rag.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddingProvider,
)
from enterprise_rag.evaluation.retrieval_metrics import (
    mean_reciprocal_rank,
    recall_at_k,
)
from enterprise_rag.reranking.cross_encoder import CrossEncoderReranker
from enterprise_rag.retrieval.service import RetrievalService
from enterprise_rag.retrieval.vector_search import VectorSearchRepository


EVALUATION_FILE = Path(
    "data/evaluation/retrieval_cases.json"
)


def load_evaluation_cases() -> list[dict]:
    return json.loads(
        EVALUATION_FILE.read_text(encoding="utf-8")
    )


def extract_retrieved_evidence(
    results,
) -> list[tuple[str, str]]:
    retrieved: list[tuple[str, str]] = []

    for result in results:
        if result.heading is None:
            continue

        retrieved.append(
            (
                result.title,
                result.heading,
            )
        )

    return retrieved


def evaluate_service(
    service: RetrievalService,
    cases: list[dict],
    service_name: str,
) -> tuple[float, float]:
    retrieved_results: list[list[tuple[str, str]]] = []
    expected_results: list[tuple[str, str]] = []

    print("\n" + "=" * 60)
    print(service_name)
    print("=" * 60)

    for case in cases:
        results = service.retrieve(
            question=case["question"],
            limit=5,
            candidate_limit=10,
            similarity_threshold=0.50,
        )

        retrieved = extract_retrieved_evidence(results)

        expected = (
            case["expected_title"],
            case["expected_heading"],
        )

        retrieved_results.append(retrieved)
        expected_results.append(expected)

        print(f"\nCase: {case['id']}")
        print(f"Question: {case['question']}")
        print(f"Expected: {expected}")
        print("Retrieved:")

        for rank, item in enumerate(
            retrieved,
            start=1,
        ):
            print(f"  {rank}. {item}")

    recall = recall_at_k(
        retrieved_results=retrieved_results,
        expected_results=expected_results,
    )

    mrr = mean_reciprocal_rank(
        retrieved_results=retrieved_results,
        expected_results=expected_results,
    )

    return recall, mrr


def main() -> None:
    cases = load_evaluation_cases()

    # Shared dependencies.
    #
    # Both retrieval configurations use exactly the same embedding
    # model and vector-search repository so that reranking is the
    # only variable changing between the two experiments.
    embedding_provider = SentenceTransformerEmbeddingProvider()
    search_repository = VectorSearchRepository()

    baseline_service = RetrievalService(
        embedding_provider=embedding_provider,
        search_repository=search_repository,
    )

    reranker = CrossEncoderReranker()

    reranked_service = RetrievalService(
        embedding_provider=embedding_provider,
        search_repository=search_repository,
        reranker=reranker,
    )

    baseline_recall, baseline_mrr = evaluate_service(
        service=baseline_service,
        cases=cases,
        service_name="Baseline Vector Retrieval",
    )

    reranked_recall, reranked_mrr = evaluate_service(
        service=reranked_service,
        cases=cases,
        service_name="Vector Retrieval + Cross-Encoder Reranking",
    )

    print("\n" + "=" * 60)
    print("Evaluation Summary")
    print("=" * 60)

    print("\nBaseline Vector Retrieval")
    print(f"Recall@5: {baseline_recall:.2%}")
    print(f"MRR:      {baseline_mrr:.4f}")

    print("\nVector Retrieval + Cross-Encoder Reranking")
    print(f"Recall@5: {reranked_recall:.2%}")
    print(f"MRR:      {reranked_mrr:.4f}")

    print("\nChange")
    print(
        f"Recall@5: "
        f"{reranked_recall - baseline_recall:+.2%}"
    )
    print(
        f"MRR:      "
        f"{reranked_mrr - baseline_mrr:+.4f}"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()