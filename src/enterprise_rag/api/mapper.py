from enterprise_rag.rag.models import RAGResponse
from enterprise_rag.api.models import AskResponse

def map_rag_response_to_api(response: RAGResponse) -> AskResponse:
    api_response = AskResponse(answer= response.answer, citations= [])
    return api_response






