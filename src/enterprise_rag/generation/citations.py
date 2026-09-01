import re


def extract_citation_indices(answer: str) -> list[int]:
    matches = re.findall(r"\[(\d+)\]", answer)

    return [int(match) for match in matches]


def find_invalid_citation_indices(
    answer: str,
    valid_indices: set[int],
) -> list[int]:
    citation_indices = extract_citation_indices(answer)

    return [
        index
        for index in citation_indices
        if index not in valid_indices
    ]