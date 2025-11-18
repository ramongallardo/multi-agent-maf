# Quick Start Guide - Microsoft Agentic Framework

This guide will get you up and running with the migrated Microsoft Agentic Framework project.

## 1. Install Dependencies

First, ensure you have Python 3.11+ installed, then install the new dependencies:

```bash
# Activate your virtual environment (if not already active)
source venv/bin/activate

# Install MAF dependencies
pip install -r requirements.txt
```

## 2. Configure Environment

Copy the example environment file and add your API key:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
MODEL_NAME=gpt-4o
```

> **Note**: For Azure OpenAI, uncomment and fill in the Azure-specific variables.

## 3. Run Your First Example

Try the simple conversation example:

```bash
python examples/simple_conversation.py
```

You should see:
- The agent receiving the task
- Streaming output of the agent's response
- Completion statistics

## 4. Explore Other Examples

### Multi-Agent Collaboration
Three agents working together (Researcher, Writer, Critic):

```bash
python examples/multi_agent_collaboration.py
```

### Agent with Tools
Agent using custom functions (math and weather tools):

```bash
python examples/agent_with_tools.py
```

### Advanced Selector Team
Dynamic agent selection based on context:

```bash
python examples/advanced_team_selector.py
```

### Observability Demo
See OpenTelemetry tracing in action:

```bash
python examples/observability_example.py
```

## 5. Key Differences from AutoGen 0.2.x

### Async/Await Required

All MAF operations are asynchronous:

```python
import asyncio

async def main():
    result = await Console(team.run_stream(task="..."))

if __name__ == "__main__":
    asyncio.run(main())
```

### No UserProxyAgent

Teams handle orchestration instead of UserProxyAgent:

```python
# Old way (AutoGen 0.2)
user_proxy.initiate_chat(assistant, message="task")

# New way (MAF)
team = RoundRobinGroupChat(participants=[assistant], ...)
await Console(team.run_stream(task="task"))
```

### Model Client vs Config Dict

Use ModelClient objects instead of config dicts:

```python
# Old way
llm_config = {"config_list": [...], "temperature": 0.7}

# New way
model_client = OpenAIChatCompletionClient(model="gpt-4o", ...)
```

## 6. Common Tasks

### Create a New Agent

```python
from autogen_agentchat.agents import AssistantAgent
from config import get_model_client

agent = AssistantAgent(
    name="MyAgent",
    model_client=get_model_client(),
    system_message="Your agent's instructions here",
)
```

### Add a Custom Tool

```python
from typing import Annotated
from autogen_core.components.tools import FunctionTool

def my_tool(x: Annotated[int, "A number"]) -> int:
    """Doubles the input number."""
    return x * 2

tool = FunctionTool(my_tool, description="Doubles a number")

agent = AssistantAgent(
    name="ToolAgent",
    model_client=get_model_client(),
    tools=[tool],
)
```

### Set Termination Conditions

```python
from autogen_agentchat.conditions import (
    TextMentionTermination,
    MaxMessageTermination,
)

# Stop when "TERMINATE" is mentioned OR after 20 messages
termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(20)
```

### Create a Multi-Agent Team

```python
team = RoundRobinGroupChat(
    participants=[agent1, agent2, agent3],
    termination_condition=termination,
)

result = await Console(team.run_stream(task="Your task"))
```

## 7. Troubleshooting

### Import Errors

If you see `ModuleNotFoundError`:
1. Ensure virtual environment is activated
2. Run `pip install -r requirements.txt`
3. Check Python version is 3.11+

### API Key Not Working

1. Check `.env` file exists in project root
2. Verify no extra spaces in `OPENAI_API_KEY=...`
3. Ensure API key is valid and has credits

### Async Errors

Remember to:
- Use `async def` for functions calling MAF
- Always `await` async operations
- Use `asyncio.run(main())` to start

### Model Not Found

Update to newer model names:
- Use `gpt-4o` instead of `gpt-4`
- Use `gpt-4-turbo` for GPT-4 Turbo
- Check [OpenAI Models](https://platform.openai.com/docs/models) for latest

## 8. Next Steps

1. **Read the Migration Guide**: See `MIGRATION_GUIDE.md` for detailed changes
2. **Explore Documentation**: [MAF Documentation](https://microsoft.github.io/autogen/)
3. **Try Custom Agents**: Create your own specialized agents
4. **Add Observability**: Explore OpenTelemetry integration
5. **Deploy to Azure**: Use Azure AI Foundry for production deployments

## 9. Getting Help

- **Documentation**: https://microsoft.github.io/autogen/stable/
- **Examples**: `examples/` directory in this project
- **Issues**: Check error messages and stack traces
- **Community**: GitHub Discussions for AutoGen

## 10. Production Checklist

Before deploying to production:

- [ ] API keys stored securely (Azure Key Vault, etc.)
- [ ] Proper error handling implemented
- [ ] Termination conditions set appropriately
- [ ] Observability/monitoring configured
- [ ] Rate limiting and cost controls in place
- [ ] Agent messages logged for audit trails
- [ ] Security review of system messages and tools
- [ ] Performance testing completed
- [ ] Fallback strategies for API failures

---

**You're ready to build with the Microsoft Agentic Framework!** 🚀

For more details, see the full README.md and MIGRATION_GUIDE.md.
