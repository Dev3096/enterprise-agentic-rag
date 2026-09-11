import pytest
from enterprise_rag.generation.exceptions import CitationValidationError, MISSING_CITATIONS, INVALID_CITATIONS

def test_custom_exception() -> None:
    error = CitationValidationError(INVALID_CITATIONS, "These are invalid citations")
    assert error.reason == INVALID_CITATIONS
    assert str(error) == "These are invalid citations"
    assert isinstance(error, ValueError)

@pytest.mark.parametrize(
    "reason", 
    [
        (MISSING_CITATIONS), 
        (INVALID_CITATIONS),
    ]
)
def test_exception(reason) -> None:
    valid_error = CitationValidationError(reason=reason, message="These are invalid citations")
    assert valid_error.reason == reason