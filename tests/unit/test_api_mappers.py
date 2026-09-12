from enterprise_rag.rag.models import RAGResponse, Citation
from enterprise_rag.api.mapper import map_rag_response_to_api
import pytest

def test_api_mapper() -> None:
    response = RAGResponse(answer= "hey, this is a test", sources= [], citations= [])
    api_response = map_rag_response_to_api(response)
    assert api_response.answer == response.answer
    assert api_response.citations == []

def test_one_citation_api_mapper() -> None:
    response = RAGResponse(answer= "TOKEN_EXPIRED errors were caused by incorrect session-cache invalidation [1].", sources= [],
                          citations= [Citation(index= 1, title= "INC-482", heading= "Root Cause", source= "incidents/INC-482.md", similarity= 0.91)])
    api_response = map_rag_response_to_api(response)
    assert len(api_response.citations) == 1
    assert api_response.citations[0].title == "INC-482"
    assert api_response.citations[0].heading == "Root Cause"
    assert api_response.citations[0].similarity == pytest.approx(0.91)

def test_multiple_citation_api_mapper() -> None:
    response = RAGResponse(answer= "TOKEN_EXPIRED errors were caused by incorrect session-cache invalidation [1].", sources= [],
                          citations= [Citation(index= 1, title= "INC-482", heading= "Root Cause", source= "incidents/INC-482.md", similarity= 0.91),
                                     Citation(index= 2, title= "V2.18", heading= "Know Issues", source= "incidents/V2,18.md", similarity= 0.97)])
    api_response = map_rag_response_to_api(response)
    assert len(api_response.citations) == 2
    assert api_response.citations[0].title == "INC-482"
    assert api_response.citations[0].heading == "Root Cause"
    assert api_response.citations[0].similarity == pytest.approx(0.91)

    assert api_response.citations[1].title == "V2.18"
    assert api_response.citations[1].heading == "Know Issues"
    assert api_response.citations[1].similarity == pytest.approx(0.97)