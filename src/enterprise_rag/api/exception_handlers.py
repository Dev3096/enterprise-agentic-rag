from fastapi import Request
from fastapi.responses import JSONResponse
from enterprise_rag.generation.exceptions import CitationValidationError


async def citation_validation_exception_handler( request: Request, exc: CitationValidationError):
    return JSONResponse(
        status_code= 500, 
        content={
            "error": exc.reason,
            "message": str(exc)
        }
    )