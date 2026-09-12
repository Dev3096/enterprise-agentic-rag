from enterprise_rag.rag.models import RAGResponse
from enterprise_rag.api.models import AskResponse
from enterprise_rag.api.models import CitationResponse

def map_rag_response_to_api(response: RAGResponse) -> AskResponse:
    api_citations = [
        CitationResponse(
            index= citation.index,
            title= citation.title,
            heading= citation.heading,
            source= citation.source,
            similarity= citation.similarity,
        ) for citation in response.citations
    ]
        

    api_response = AskResponse(answer= response.answer, citations= api_citations)
    return api_response






