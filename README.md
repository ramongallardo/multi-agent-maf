# Multi-Agent Agentic Framework (MAF)

A Python-based multi-agent system built with the **Microsoft Agentic Framework** for creating collaborative AI agents with enterprise-grade observability and orchestration.

## Overview

This project provides a foundation for building multi-agent systems where AI agents can collaborate, communicate, and solve complex tasks together. It uses the **Microsoft Agentic Framework (MAF)** - the successor to Semantic Kernel and AutoGen - combining modern orchestration patterns with built-in observability for enterprise use cases.

## Features

- **Modern Agent Types**: AssistantAgent with enhanced capabilities and custom agent support
- **Team Orchestration**: Built-in team patterns (RoundRobinGroupChat, SelectorGroupChat) for collaboration
- **Custom Tools**: Extend agents with FunctionTools and custom capabilities
- **Flexible Model Clients**: Easy configuration for OpenAI or Azure OpenAI with ModelClient pattern
- **Enterprise Observability**: Built-in OpenTelemetry integration for monitoring and tracing
- **Async-First Design**: Modern async/await patterns for better performance
- **Ready-to-Run Examples**: Pre-built examples demonstrating various multi-agent patterns

## Project Structure

```
multi-agent-maf/
├── agents/              # Agent definitions and custom agents
├── config/              # Configuration files for LLM and agents
│   ├── llm_config.py   # LLM configuration utilities
│   └── __init__.py
├── tools/               # Custom tools and functions for agents
├── examples/            # Example multi-agent scenarios
│   ├── simple_conversation.py          # Basic two-agent conversation
│   ├── multi_agent_collaboration.py    # Multi-agent group chat
│   └── agent_with_tools.py             # Agent with custom tools
├── .env.example         # Environment variable template
├── .gitignore          # Git ignore file
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Prerequisites

- Python 3.11 or higher
- OpenAI API key or Azure OpenAI credentials
- Virtual environment (recommended)
- Basic understanding of async/await in Python

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd multi-agent-maf
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API credentials:
   ```
   # OpenAI Configuration
   OPENAI_API_KEY=your_openai_api_key_here
   MODEL_NAME=gpt-4o
   
   # Azure OpenAI Configuration (optional)
   AZURE_OPENAI_API_KEY=your_azure_key_here
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_MODEL_DEPLOYMENT_NAME=gpt-4
   AZURE_OPENAI_API_VERSION=2024-02-15-preview
   ```

## Quick Start

### Running Examples

1. **Simple Conversation** - A basic two-agent conversation:
   ```bash
   python examples/simple_conversation.py
   ```

2. **Multi-Agent Collaboration** - Agents working together (Researcher, Writer, Critic):
   ```bash
   python examples/multi_agent_collaboration.py
   ```

3. **Agent with Custom Tools** - An agent using custom functions:
   ```bash
   python examples/agent_with_tools.py
   ```

### Creating Your Own Agents

Here's a minimal example to get started:

```python
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination
from config import get_model_client

async def main():
    # Get model client
    model_client = get_model_client()
    
    # Create assistant agent
    assistant = AssistantAgent(
        name="Assistant",
        model_client=model_client,
        system_message="You are a helpful assistant.",
    )
    
    # Create team with termination condition
    team = RoundRobinGroupChat(
        participants=[assistant],
        termination_condition=MaxMessageTermination(10),
    )
    
    # Run conversation
    await Console(team.run_stream(task="Your task here"))

if __name__ == "__main__":
    asyncio.run(main())
```

## Configuration

### Model Client Configuration

The project supports both OpenAI and Azure OpenAI via ModelClient pattern:

**OpenAI**:
```python
from config import get_model_client
model_client = get_model_client()  # Uses OpenAI by default
```

**Azure OpenAI**:
```python
from config import get_model_client
model_client = get_model_client(use_azure=True)
```

Configure your credentials in `.env`:
- `OPENAI_API_KEY` - Your OpenAI API key
- `MODEL_NAME` - Model to use (e.g., gpt-4o, gpt-4-turbo)
- `AZURE_OPENAI_API_KEY` - Your Azure OpenAI key (if using Azure)
- `AZURE_OPENAI_ENDPOINT` - Your Azure endpoint (if using Azure)
- `AZURE_MODEL_DEPLOYMENT_NAME` - Your Azure model deployment name

### Agent Configuration

Agents can be configured with various parameters:

- **model_client**: The LLM client for the agent (OpenAI or Azure)
- **system_message**: Instructions defining the agent's role and behavior
- **tools**: List of FunctionTool instances the agent can use
- **description**: Agent description for team-based selection

### Team Configuration

Teams orchestrate multiple agents:

- **RoundRobinGroupChat**: Agents take turns in order
- **SelectorGroupChat**: Dynamic agent selection based on context
- **termination_condition**: When to stop (TextMentionTermination, MaxMessageTermination, etc.)

## Development

### Adding Custom Tools

Create custom tools in the `tools/` directory:

```python
from typing import Annotated
from autogen_core.components.tools import FunctionTool

def my_custom_tool(param: Annotated[str, "Parameter description"]) -> str:
    """Tool description for the agent."""
    # Your implementation
    return result

# Create FunctionTool instance
tool = FunctionTool(
    my_custom_tool,
    description="Detailed tool description"
)
```

Register tools with agents:

```python
assistant = AssistantAgent(
    name="Assistant",
    model_client=model_client,
    tools=[tool],  # Pass tools as list
)
```

### Creating Specialized Agents

Define specialized agents in the `agents/` directory with custom system messages and capabilities:

```python
researcher = AssistantAgent(
    name="Researcher",
    model_client=model_client,
    system_message="You are a research specialist...",
    description="Specializes in research and fact-finding",
)
```

## Best Practices

- Store API keys in environment variables, never in code
- Use type hints for all function parameters (required for FunctionTool)
- Document agent behaviors and system messages clearly
- Test agents individually before combining in teams
- Use async/await patterns consistently throughout your code
- Leverage OpenTelemetry for monitoring and debugging
- Monitor token usage for cost optimization
- Use appropriate temperature settings for your use case
- Set proper termination conditions to prevent infinite loops
- Use Console UI for streaming output in development

## Troubleshooting

### Import Errors
If you see import errors for `autogen_agentchat` or other MAF modules, ensure you've:
1. Activated the virtual environment
2. Installed dependencies: `pip install -r requirements.txt`
3. Using Python 3.11 or higher

### API Key Issues
- Verify your `.env` file is in the project root
- Check that API keys are valid and have sufficient credits
- Ensure no extra spaces or quotes around keys in `.env`
- For Azure: verify endpoint URL and deployment name are correct

### Agent Not Responding
- Check your model name is correct (e.g., gpt-4o, gpt-4-turbo)
- Verify network connectivity
- Review error messages in console output
- Check OpenTelemetry traces for detailed execution flow

### Async Issues
- Ensure you're using `asyncio.run()` to start async main functions
- Use `await` for all async operations
- Don't mix sync and async code without proper handling

## Resources

- [Microsoft Agentic Framework Documentation](https://microsoft.github.io/autogen/)
- [AutoGen 0.4 Documentation](https://microsoft.github.io/autogen/stable/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
- [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/)
- [Azure AI Foundry](https://azure.microsoft.com/en-us/products/ai-studio/)

## License

This project is provided as-is for educational and development purposes.

## Contributing

Feel free to extend this framework with:
- New agent types and roles
- Additional custom tools
- More sophisticated examples
- Integration with external APIs and services

---

**Happy Agent Building!** 🤖
