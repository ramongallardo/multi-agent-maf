"""LLM configuration for Microsoft Agentic Framework agents."""
import os
from typing import Optional
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient, AzureOpenAIChatCompletionClient
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor

# Load environment variables
load_dotenv()

# Initialize OpenTelemetry for observability
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
span_processor = BatchSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)


def get_openai_client() -> OpenAIChatCompletionClient:
    """Get OpenAI model client for MAF agents.
    
    Returns:
        OpenAI chat completion client configured with environment variables
    """
    return OpenAIChatCompletionClient(
        model=os.getenv("MODEL_NAME", "gpt-4o"),
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.7,
        timeout=120,
    )


def get_azure_openai_client() -> AzureOpenAIChatCompletionClient:
    """Get Azure OpenAI model client for MAF agents.
    
    Returns:
        Azure OpenAI chat completion client configured with environment variables
    """
    return AzureOpenAIChatCompletionClient(
        model=os.getenv("AZURE_MODEL_DEPLOYMENT_NAME", "gpt-4"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        temperature=0.7,
        timeout=120,
    )


def get_model_client(use_azure: bool = False):
    """Get model client based on provider.
    
    Args:
        use_azure: Whether to use Azure OpenAI (default: False)
        
    Returns:
        Configured model client for MAF agents
    """
    if use_azure:
        return get_azure_openai_client()
    return get_openai_client()


def get_tracer():
    """Get OpenTelemetry tracer for agent observability.
    
    Returns:
        OpenTelemetry tracer instance
    """
    return tracer
