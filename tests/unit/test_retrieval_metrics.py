from enterprise_rag.evaluation.retrieval_metrics import recall_at_k


def test_recall_at_k_all_hits():
    retrieved_results = [
        [
            ("INC-482", "Symptoms"),
            ("INC-482", "Root Cause"),
        ],
        [
            ("login_failures", "TOKEN_EXPIRED Errors"),
        ],
    ]

    expected_results = [
        ("INC-482", "Root Cause"),
        ("login_failures", "TOKEN_EXPIRED Errors"),
    ]

    recall = recall_at_k(
        retrieved_results=retrieved_results,
        expected_results=expected_results,
    )

    assert recall == 1.0


def test_recall_at_k_partial_hits():
    retrieved_results = [
        [
            ("INC-482", "Symptoms"),
            ("INC-482", "Root Cause"),
        ],
        [
            ("authentication", "Authentication Errors"),
        ],
    ]

    expected_results = [
        ("INC-482", "Root Cause"),
        ("login_failures", "TOKEN_EXPIRED Errors"),
    ]

    recall = recall_at_k(
        retrieved_results=retrieved_results,
        expected_results=expected_results,
    )

    assert recall == 0.5


def test_recall_at_k_no_expected_results():
    recall = recall_at_k(
        retrieved_results=[],
        expected_results=[],
    )

    assert recall == 0.0

import pytest

from enterprise_rag.evaluation.retrieval_metrics import (
    mean_reciprocal_rank,
    recall_at_k,
)


def test_mean_reciprocal_rank_all_first_place():
    retrieved_results = [
        [
            ("INC-482", "Root Cause"),
            ("INC-482", "Symptoms"),
        ],
        [
            ("login_failures", "TOKEN_EXPIRED Errors"),
            ("v2.18", "Known Issues"),
        ],
    ]

    expected_results = [
        ("INC-482", "Root Cause"),
        ("login_failures", "TOKEN_EXPIRED Errors"),
    ]

    mrr = mean_reciprocal_rank(
        retrieved_results=retrieved_results,
        expected_results=expected_results,
    )

    assert mrr == 1.0


def test_mean_reciprocal_rank_mixed_ranks():
    retrieved_results = [
        [
            ("INC-482", "Symptoms"),
            ("INC-482", "Root Cause"),
        ],
        [
            ("authentication", "Authentication Errors"),
            ("v2.18", "Known Issues"),
            ("login_failures", "TOKEN_EXPIRED Errors"),
        ],
    ]

    expected_results = [
        ("INC-482", "Root Cause"),
        ("login_failures", "TOKEN_EXPIRED Errors"),
    ]

    mrr = mean_reciprocal_rank(
        retrieved_results=retrieved_results,
        expected_results=expected_results,
    )

    expected_mrr = ((1 / 2) + (1 / 3)) / 2

    assert mrr == pytest.approx(expected_mrr)


def test_mean_reciprocal_rank_missing_result():
    retrieved_results = [
        [
            ("INC-482", "Symptoms"),
        ],
        [
            ("login_failures", "TOKEN_EXPIRED Errors"),
        ],
    ]

    expected_results = [
        ("INC-482", "Root Cause"),
        ("login_failures", "TOKEN_EXPIRED Errors"),
    ]

    mrr = mean_reciprocal_rank(
        retrieved_results=retrieved_results,
        expected_results=expected_results,
    )

    expected_mrr = (0 + 1) / 2

    assert mrr == pytest.approx(expected_mrr)