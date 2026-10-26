import pytest
from app.services.llm.base import LLMProvider
from app.services.llm.mock_provider import MockLLMProvider
from app.services.llm.openai_provider import OpenAIProvider
from app.services.llm.service import LLMService


@pytest.mark.asyncio
async def test_mock_llm_provider():
    mock = MockLLMProvider(responses=["Custom generated answer"])
    res = await mock.generate(prompt="Hello", context="Context")
    assert res == "Custom generated answer"
    assert len(mock.calls) == 1
    assert mock.calls[0]["prompt"] == "Hello"
    assert mock.calls[0]["context"] == "Context"


@pytest.mark.asyncio
async def test_llm_service_with_explicit_provider():
    mock = MockLLMProvider(default_response="Echoed text")
    service = LLMService(provider=mock)
    res = await service.generate(prompt="Summarize role", context="Job posting")
    assert res == "Echoed text"


@pytest.mark.asyncio
async def test_llm_service_failover_chain():
    class FailingProvider(LLMProvider):
        async def generate(self, prompt: str, context=None, **kwargs):
            raise RuntimeError("Primary API rate limited / down")

    failing = FailingProvider()
    fallback = MockLLMProvider(default_response="Fallback successful response")

    # Create a service with two providers in chain
    service = LLMService()
    service._resolve_providers = lambda: [failing, fallback]

    res = await service.generate(prompt="Test fallback")
    assert res == "Fallback successful response"


@pytest.mark.asyncio
async def test_openai_provider_missing_key():
    prov = OpenAIProvider(api_key="")
    with pytest.raises(ValueError, match="OpenAI API key is missing"):
        await prov.generate(prompt="Test")
