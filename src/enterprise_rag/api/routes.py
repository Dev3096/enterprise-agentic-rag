from fastapi import APIRouter
from enterprise_rag.api.models import AskResponse, AskRequest

router = APIRouter()

@router.post("/ask", response_model= AskResponse)
async def ask_router(request: AskRequest) -> AskResponse:
    return AskResponse(answer= "This is the response", citations= [])