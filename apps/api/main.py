from fastapi import FastAPI
from enterprise_rag.api.routes import router
from enterprise_rag.generation.exceptions import CitationValidationError
from enterprise_rag.api.exception_handlers import citation_validation_exception_handler

app = FastAPI(
    title="Enterprise Agentic RAG",
    description="Production-grade enterprise agentic RAG platform",
    version="0.1.0",
)

app.include_router(router)
app.add_exception_handler(CitationValidationError, citation_validation_exception_handler)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "enterprise-agentic-rag",
        "version": "0.1.0",
    }