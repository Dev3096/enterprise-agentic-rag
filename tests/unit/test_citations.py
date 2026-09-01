from enterprise_rag.generation.citations import (
    extract_citation_indices,
    find_invalid_citation_indices,
)


def test_extract_citation_indices() -> None:
    answer = (
        "The session cache caused the issue [1]. "
        "Version 2.18 introduced the behavior [2]."
    )

    result = extract_citation_indices(answer)

    assert result == [1, 2]


def test_extract_citation_indices_returns_empty_list_when_none_present() -> None:
    answer = "The session cache caused the issue."

    result = extract_citation_indices(answer)

    assert result == []


def test_find_invalid_citation_indices() -> None:
    answer = (
        "The issue was caused by the cache [1]. "
        "Another unsupported claim uses [7]."
    )

    result = find_invalid_citation_indices(
        answer=answer,
        valid_indices={1, 2, 3},
    )

    assert result == [7]


def test_find_invalid_citation_indices_returns_empty_when_all_valid() -> None:
    answer = "The issue was caused by the cache [1] and documented in [2]."

    result = find_invalid_citation_indices(
        answer=answer,
        valid_indices={1, 2},
    )

    assert result == []