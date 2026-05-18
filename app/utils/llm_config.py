from crewai import LLM

from app.config.settings import (
    OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_DEPLOYMENT
)

azure_llm = LLM(
    model=f"azure/{AZURE_OPENAI_DEPLOYMENT}",

    api_key=OPENAI_API_KEY,

    base_url=(
        f"{AZURE_OPENAI_ENDPOINT}"
        "openai/deployments/"
        f"{AZURE_OPENAI_DEPLOYMENT}"
    ),

    api_version="2024-02-15-preview"
)