def recall_at_k(
    retrieved_results: list[list[tuple[str, str]]],
    expected_results: list[tuple[str, str]],
) -> float:
    if not expected_results:
        return 0.0

    hits = 0

    for retrieved, expected in zip(
        retrieved_results,
        expected_results,
        strict=True,
    ):
        if expected in retrieved:
            hits += 1

    return hits / len(expected_results)

def mean_reciprocal_rank(
    retrieved_results: list[list[tuple[str, str]]],
    expected_results: list[tuple[str, str]],
) -> float:
    if not expected_results:
        return 0.0

    reciprocal_ranks: list[float] = []

    for retrieved, expected in zip(
        retrieved_results,
        expected_results,
        strict=True,
    ):
        reciprocal_rank = 0.0

        for rank, result in enumerate(
            retrieved,
            start=1,
        ):
            if result == expected:
                reciprocal_rank = 1 / rank
                break

        reciprocal_ranks.append(reciprocal_rank)

    return sum(reciprocal_ranks) / len(reciprocal_ranks)