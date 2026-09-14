from fastapi import FastAPI
from enterprise_rag.api.routes import router

app = FastAPI(
    title="Enterprise Agentic RAG",
    description="Production-grade enterprise agentic RAG platform",
    version="0.1.0",
)

app.include_router(router)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "enterprise-agentic-rag",
        "version": "0.1.0",
    }