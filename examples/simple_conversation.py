"""Simple two-agent conversation example using Microsoft Agentic Framework."""
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from config import get_model_client, get_tracer


async def main():
    """Run a simple conversation between two agents."""
    
    # Get model client and tracer
    model_client = get_model_client()
    tracer = get_tracer()
    
    with tracer.start_as_current_span("simple_conversation"):
        # Create an assistant agent
        assistant = AssistantAgent(
            name="Assistant",
            model_client=model_client,
            system_message="You are a helpful AI assistant. Help the user with their tasks. When the story is complete, say TERMINATE.",
        )
        
        # Create termination condition
        termination = TextMentionTermination("TERMINATE")
        
        # Create a team with the assistant
        team = RoundRobinGroupChat(
            participants=[assistant],
            termination_condition=termination,
        )
        
        # Run the conversation
        print("Starting conversation...\n")
        result = await Console(
            team.run_stream(
                task="Tell me a brief story about AI agents working together to solve a problem."
            )
        )
        
        print(f"\nConversation completed. Messages exchanged: {len(result.messages)}")


if __name__ == "__main__":
    asyncio.run(main())
