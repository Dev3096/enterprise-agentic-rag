from enterprise_rag.api.models import AskRequest
from pydantic import ValidationError
import pytest

def test_request_model() -> None:
    request = AskRequest(question= "Why are TOKEN_EXPIRED errors increasing?")
    assert request.question == "Why are TOKEN_EXPIRED errors increasing?"

def test_request_model_no_question_asked_raises_exception() -> None:
    with pytest.raises(ValidationError):
        AskRequest()

def test_request_model_empty_string() -> None:
    with pytest.raises(ValidationError):
        AskRequest(question="")

def test_request_model_empty_string_whitespaces() -> None:
    with pytest.raises(ValidationError):
        AskRequest(question="   ")


    
