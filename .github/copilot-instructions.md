# Multi-Agent Agentic Framework Project

## Project Overview
This project uses the **Microsoft Agentic Framework (MAF)** - AutoGen 0.4+ - to build enterprise-ready multi-agent systems in Python. MAF is the successor to Semantic Kernel and AutoGen, combining modern orchestration with built-in observability.

## Technology Stack
- Python 3.11+
- autogen-agentchat 0.4+ (Microsoft Agentic Framework)
- autogen-ext with OpenAI and Azure extensions
- OpenAI API or Azure OpenAI
- OpenTelemetry for observability

## Project Structure
- `agents/` - Agent definitions and configurations
- `tools/` - Custom tools and functions for agents (use FunctionTool pattern)
- `config/` - Configuration files for model clients and observability
- `examples/` - Example multi-agent scenarios using MAF patterns

## Key Framework Patterns

### Model Client Pattern
Use `ModelClient` instead of config dicts:
```python
from autogen_ext.models import OpenAIChatCompletionClient

model_client = OpenAIChatCompletionClient(
    model="gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY"),
)
```

### Agent Creation
```python
from autogen_agentchat.agents import AssistantAgent

agent = AssistantAgent(
    name="AgentName",
    model_client=model_client,
    system_message="Agent instructions",
    tools=[tool1, tool2],  # Optional FunctionTool instances
)
```

### Team Orchestration
Use team patterns instead of UserProxyAgent:
```python
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination

team = RoundRobinGroupChat(
    participants=[agent1, agent2],
    termination_condition=MaxMessageTermination(20),
)

await Console(team.run_stream(task="Your task"))
```

### Tool Registration
Use FunctionTool pattern:
```python
from autogen_core.components.tools import FunctionTool

tool = FunctionTool(
    my_function,
    description="What this tool does"
)

agent = AssistantAgent(
    name="Agent",
    model_client=model_client,
    tools=[tool],
)
```

## Development Guidelines
- **Always use async/await**: MAF is async-first
- Follow Python best practices (PEP 8)
- Use type hints for all function parameters (required for FunctionTool)
- Document agent behaviors and system messages clearly
- Store API keys in environment variables, never in code
- Always set termination conditions to prevent infinite loops
- Use OpenTelemetry for observability and debugging
- Prefer Console UI for development streaming output
