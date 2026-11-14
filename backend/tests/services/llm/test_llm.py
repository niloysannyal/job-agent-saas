from unittest.mock import AsyncMock, MagicMock, patch
import pytest

from app.core.crypto import encrypt_secret
from app.models.llm_provider import LLMProviderConfig
from app.services.llm.base import LLMProvider
from app.services.llm.mock_provider import MockLLMProvider
from app.services.llm.openai_provider import OpenAIProvider
from app.services.llm.anthropic_provider import AnthropicProvider
from app.services.llm.gemini_provider import GeminiProvider
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


@pytest.mark.asyncio
async def test_anthropic_provider_missing_key():
    prov = AnthropicProvider(api_key="")
    with pytest.raises(ValueError, match="Anthropic API key is missing"):
        await prov.generate(prompt="Test")


@pytest.mark.asyncio
async def test_anthropic_provider_generate_success():
    prov = AnthropicProvider(api_key="sk-ant-test-key", model_name="claude-3-5-sonnet-20241022")

    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "content": [
            {"type": "text", "text": "Claude tailored CV successfully"}
        ]
    }
    mock_resp.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_resp
        res = await prov.generate(prompt="Tailor bullet points", context="Job Context")
        assert res == "Claude tailored CV successfully"

        # Check call arguments
        call_kwargs = mock_post.call_args.kwargs
        assert call_kwargs["headers"]["x-api-key"] == "sk-ant-test-key"
        assert call_kwargs["json"]["model"] == "claude-3-5-sonnet-20241022"
        assert call_kwargs["json"]["system"] == "Job Context"
        assert call_kwargs["json"]["messages"] == [{"role": "user", "content": "Tailor bullet points"}]


@pytest.mark.asyncio
async def test_gemini_provider_missing_key():
    prov = GeminiProvider(api_key="")
    with pytest.raises(ValueError, match="Gemini API key is missing"):
        await prov.generate(prompt="Test")


@pytest.mark.asyncio
async def test_gemini_provider_generate_success():
    prov = GeminiProvider(api_key="ai-za-test-key", model_name="gemini-2.5-flash")

    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "candidates": [
            {
                "content": {
                    "parts": [{"text": "Gemini analyzed fit: 92/100"}]
                }
            }
        ]
    }
    mock_resp.raise_for_status = MagicMock()

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_resp
        res = await prov.generate(prompt="Score alignment", context="Senior Backend Engineer")
        assert res == "Gemini analyzed fit: 92/100"

        # Check call arguments
        call_kwargs = mock_post.call_args.kwargs
        assert call_kwargs["params"]["key"] == "ai-za-test-key"
        assert call_kwargs["json"]["systemInstruction"] == {"parts": [{"text": "Senior Backend Engineer"}]}
        assert call_kwargs["json"]["contents"] == [{"role": "user", "parts": [{"text": "Score alignment"}]}]


@pytest.mark.asyncio
async def test_llm_service_gemini_claude_openai_failover():
    """Verify 3-tier failover: Gemini (priority 1 fails) -> Claude (priority 2 fails) -> OpenAI succeeds."""
    class FailingGemini(LLMProvider):
        async def generate(self, prompt: str, context=None, **kwargs):
            raise RuntimeError("Gemini 429 quota exhausted")

    class FailingClaude(LLMProvider):
        async def generate(self, prompt: str, context=None, **kwargs):
            raise RuntimeError("Claude 529 overloaded")

    class BedrockOpenAI(LLMProvider):
        async def generate(self, prompt: str, context=None, **kwargs):
            return "OpenAI Bedrock saved the run"

    service = LLMService()
    service._resolve_providers = lambda: [FailingGemini(), FailingClaude(), BedrockOpenAI()]

    result = await service.generate(prompt="Generate outreach")
    assert result == "OpenAI Bedrock saved the run"


def test_llm_service_db_provider_decryption_and_resolution():
    """Verify that encrypted API keys stored in DB are decrypted and resolved into provider instances."""
    enc_openai = encrypt_secret("sk-secret-openai")
    enc_claude = encrypt_secret("sk-secret-claude")
    enc_gemini = encrypt_secret("ai-secret-gemini")

    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_db.query.return_value = mock_query
    mock_query.filter.return_value = mock_query

    cfg1 = LLMProviderConfig(id="1", provider="gemini", model_name="gemini-2.5-flash", encrypted_api_key=enc_gemini, priority=1, is_active=True)
    cfg2 = LLMProviderConfig(id="2", provider="anthropic", model_name="claude-3-5-sonnet", encrypted_api_key=enc_claude, priority=2, is_active=True)
    cfg3 = LLMProviderConfig(id="3", provider="openai", model_name="gpt-4o", encrypted_api_key=enc_openai, priority=3, is_active=True)

    mock_query.order_by.return_value.all.return_value = [cfg1, cfg2, cfg3]

    service = LLMService(db_session=mock_db)
    providers = service._resolve_providers()

    # Providers order matches priority: Gemini -> Anthropic -> OpenAI
    assert isinstance(providers[0], GeminiProvider)
    assert providers[0].api_key == "ai-secret-gemini"
    assert providers[0].model_name == "gemini-2.5-flash"

    assert isinstance(providers[1], AnthropicProvider)
    assert providers[1].api_key == "sk-secret-claude"
    assert providers[1].model_name == "claude-3-5-sonnet"

    assert isinstance(providers[2], OpenAIProvider)
    assert providers[2].api_key == "sk-secret-openai"
    assert providers[2].model_name == "gpt-4o"
