# Migration Guide: AutoGen to Microsoft Agentic Framework

This guide explains the key changes when migrating from AutoGen 0.2.x to the Microsoft Agentic Framework (AutoGen 0.4+).

## Overview

The Microsoft Agentic Framework (MAF) is the evolution of AutoGen, combining the best of Semantic Kernel and AutoGen with enhanced enterprise features.

## Key Architectural Changes

### 1. Dependencies

**Before (AutoGen 0.2.x):**
```python
pyautogen>=0.2.0
openai>=1.0.0
```

**After (MAF/AutoGen 0.4):**
```python
autogen-agentchat~=0.4
autogen-ext[openai,azure]~=0.4
azure-ai-projects>=1.0.0
```

### 2. LLM Configuration

**Before:**
```python
llm_config = {
    "config_list": [{
        "model": "gpt-4",
        "api_key": os.getenv("OPENAI_API_KEY"),
    }],
    "temperature": 0.7,
}
```

**After:**
```python
from autogen_ext.models import OpenAIChatCompletionClient

model_client = OpenAIChatCompletionClient(
    model="gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.7,
)
```

### 3. Agent Creation

**Before:**
```python
assistant = autogen.AssistantAgent(
    name="Assistant",
    llm_config=llm_config,
    system_message="You are a helpful assistant.",
)

user_proxy = autogen.UserProxyAgent(
    name="UserProxy",
    human_input_mode="TERMINATE",
)
```

**After:**
```python
from autogen_agentchat.agents import AssistantAgent

assistant = AssistantAgent(
    name="Assistant",
    model_client=model_client,
    system_message="You are a helpful assistant.",
)

# UserProxyAgent is replaced by team orchestration patterns
```

### 4. Conversation Initiation

**Before (Synchronous):**
```python
user_proxy.initiate_chat(
    assistant,
    message="Hello, agent!",
)
```

**After (Asynchronous):**
```python
from autogen_agentchat.ui import Console
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination

team = RoundRobinGroupChat(
    participants=[assistant],
    termination_condition=MaxMessageTermination(10),
)

await Console(team.run_stream(task="Hello, agent!"))
```

### 5. Group Chat / Multi-Agent Collaboration

**Before:**
```python
groupchat = autogen.GroupChat(
    agents=[user_proxy, agent1, agent2, agent3],
    messages=[],
    max_round=20,
)

manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config,
)

user_proxy.initiate_chat(manager, message="Task description")
```

**After:**
```python
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination

termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(20)

team = RoundRobinGroupChat(
    participants=[agent1, agent2, agent3],
    termination_condition=termination,
)

await Console(team.run_stream(task="Task description"))
```

### 6. Tool/Function Registration

**Before:**
```python
def my_tool(x: int) -> int:
    return x * 2

autogen.register_function(
    my_tool,
    caller=assistant,
    executor=user_proxy,
    description="Doubles a number",
)
```

**After:**
```python
from autogen_core.components.tools import FunctionTool

def my_tool(x: int) -> int:
    return x * 2

tool = FunctionTool(my_tool, description="Doubles a number")

assistant = AssistantAgent(
    name="Assistant",
    model_client=model_client,
    tools=[tool],
)
```

## New Features in MAF

### 1. Built-in Observability

MAF includes OpenTelemetry integration out of the box:

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("agent_operation"):
    # Your agent code here
    result = await team.run_stream(task="...")
```

### 2. Team Patterns

Multiple built-in orchestration patterns:

- **RoundRobinGroupChat**: Agents take turns in sequential order
- **SelectorGroupChat**: Dynamic agent selection based on context
- **Custom Teams**: Build your own orchestration logic

### 3. Termination Conditions

Flexible, composable termination conditions:

```python
from autogen_agentchat.conditions import (
    TextMentionTermination,
    MaxMessageTermination,
    StopMessageTermination,
)

# Combine conditions with operators
termination = (
    TextMentionTermination("TERMINATE") | 
    MaxMessageTermination(50)
)
```

### 4. Streaming Output

Built-in streaming support with Console UI:

```python
from autogen_agentchat.ui import Console

# Automatically streams agent messages to console
await Console(team.run_stream(task="Your task"))
```

## Migration Checklist

- [ ] Update `requirements.txt` with new dependencies
- [ ] Install new packages: `pip install -r requirements.txt`
- [ ] Replace `llm_config` dicts with `ModelClient` instances
- [ ] Convert `AssistantAgent` to use `model_client` parameter
- [ ] Replace `UserProxyAgent` with team orchestration patterns
- [ ] Replace `GroupChat` + `GroupChatManager` with team patterns
- [ ] Update tool registration to use `FunctionTool`
- [ ] Convert synchronous code to async/await patterns
- [ ] Replace `initiate_chat()` with `team.run_stream()`
- [ ] Add proper termination conditions
- [ ] Add `.env` file with updated environment variables
- [ ] Test all agent interactions
- [ ] Add observability/telemetry (optional but recommended)

## Common Pitfalls

### 1. Forgetting to Use Async

MAF is async-first. Always use `asyncio.run()` and `await`:

```python
import asyncio

async def main():
    # Your async agent code
    await Console(team.run_stream(task="..."))

if __name__ == "__main__":
    asyncio.run(main())
```

### 2. Missing Termination Conditions

Always set a termination condition to prevent infinite loops:

```python
# Bad - could run forever
team = RoundRobinGroupChat(participants=[agent1, agent2])

# Good - will stop after 20 messages
team = RoundRobinGroupChat(
    participants=[agent1, agent2],
    termination_condition=MaxMessageTermination(20),
)
```

### 3. Incorrect Model Names

MAF uses newer model names. Update your `.env`:

```bash
# Old
MODEL_NAME=gpt-4

# New (recommended)
MODEL_NAME=gpt-4o  # or gpt-4-turbo
```

## Benefits of Migration

✅ **Better Performance**: Async architecture for improved concurrency  
✅ **Enterprise Ready**: Built-in observability and monitoring  
✅ **Simplified API**: More intuitive agent and team patterns  
✅ **Azure Integration**: Native support for Azure AI services  
✅ **Active Development**: Long-term Microsoft support  
✅ **Modern Python**: Leverages latest Python async features  

## Getting Help

- [Microsoft Agentic Framework Documentation](https://microsoft.github.io/autogen/)
- [AutoGen 0.4 Documentation](https://microsoft.github.io/autogen/stable/)
- [GitHub Discussions](https://github.com/microsoft/autogen/discussions)
- [Sample Code](https://github.com/microsoft/autogen/tree/main/python/packages/autogen-agentchat/examples)

## Version Support

- **AutoGen 0.2.x**: Legacy, limited support
- **AutoGen 0.4.x (MAF)**: Current, actively developed
- **Migration Period**: Both versions can coexist during transition

---

This migration brings your multi-agent system to the cutting edge of Microsoft's agentic AI platform!
