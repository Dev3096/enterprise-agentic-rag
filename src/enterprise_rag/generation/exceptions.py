from typing import Literal

INVALID_CITATIONS = "invalid_citations"
MISSING_CITATIONS = "missing_citations"

CitationValidationReason = Literal[INVALID_CITATIONS, MISSING_CITATIONS]

class CitationValidationError(ValueError):
    """Raised when a generated answer fails citation validation."""
    def __init__(self, reason: CitationValidationReason, message: str):
        super().__init__(message)
        self.reason = reason


