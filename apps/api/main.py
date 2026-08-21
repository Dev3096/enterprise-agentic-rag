from fastapi import FastAPI

app = FastAPI(
    title="Enterprise Agentic RAG",
    description="Production-grade enterprise agentic RAG platform",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "enterprise-agentic-rag",
        "version": "0.1.0",
    }