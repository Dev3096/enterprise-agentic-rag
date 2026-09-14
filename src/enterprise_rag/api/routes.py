from fastapi import APIRouter, Depends
from enterprise_rag.api.models import AskResponse, AskRequest
from enterprise_rag.rag.service import RAGService
from enterprise_rag.api.dependencies import get_rag_service
from enterprise_rag.api.mapper import map_rag_response_to_api

router = APIRouter()

@router.post("/ask", response_model= AskResponse)
async def ask_router(request: AskRequest, rag_service: RAGService = Depends(get_rag_service)) -> AskResponse:
    rag_response = rag_service.answer(request.question)
    ask_response = map_rag_response_to_api(rag_response)
    return ask_response