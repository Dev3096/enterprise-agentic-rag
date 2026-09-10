INVALID_CITATIONS = "invalid_citations"
MISSING_CITATIONS = "missing_citations"

class CitationValidationError(ValueError):
    """Raised when a generated answer fails citation validation."""
    def __init__(self, reason: str, message: str):
        super().__init__(message)
        self.reason = reason


