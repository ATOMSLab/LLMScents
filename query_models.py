# -*- coding: utf-8 -*-
__author__ = "Alexander Haibel, Github@ahaibel"

from api_key import (
    ANTHROPIC_API_KEY,
    GOOGLE_GENAI_API_KEY,
    HUGGINGFACE_API_KEY,
    OPENAI_API_KEY,
)

MODEL_PROVIDERS = {
    "anthropic": {
        "claude-opus-4-6",
        "claude-sonnet-4-5",
        # "claude-sonnet-4-5-20250929",
        "claude-haiku-4-5",
        # "claude-haiku-4-5-20251001",
    },
    "fireworks": {
        "Qwen/Qwen3-Coder-480B-A35B-Instruct",
        "Qwen/Qwen3-235B-A22B-Instruct-2507",
        "Qwen/Qwen3-235B-A22B-Thinking-2507",
        "Qwen/Qwen3-235B-A22B",
    },
    "google_genai": {
        "gemini-2.5-flash",
    },
    "novita": {
        "deepseek-ai/DeepSeek-V3.2-Exp",
        "zai-org/GLM-4.5",
        "zai-org/GLM-4.6",
    },
    "openai": {
        "gpt-5.2-codex",
        "gpt-5.2-pro",
        "gpt-5.2",
        "gpt-5",
        "gpt-5-mini",
        "gpt-5-nano",
        "gpt-oss-120b",
        "gpt-oss-20b",
    },
}


def get_model_provider(model_name: str) -> tuple[str, str]:
    api_key = ""
    model_provider = ""
    for provider, models in MODEL_PROVIDERS.items():
        if model_name in models:
            model_provider = provider

    if model_provider == "anthropic":
        api_key = ANTHROPIC_API_KEY
    if model_provider == "google_genai":
        api_key = GOOGLE_GENAI_API_KEY
    if model_provider in {"fireworks", "novita"}:
        api_key = HUGGINGFACE_API_KEY
    if model_provider == "openai":
        api_key = OPENAI_API_KEY

    return model_provider, api_key


if __name__ == "__main__":
    print(get_model_provider("zai-org/GLM-4.6"))
