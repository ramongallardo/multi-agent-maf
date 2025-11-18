"""Example demonstrating observability features in MAF using OpenTelemetry."""
import asyncio
import os
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from config import get_model_client, get_tracer


async def main():
    """Run agents with comprehensive observability and tracing."""
    
    # Get model client and tracer
    model_client = get_model_client()
    tracer = get_tracer()
    
    # Create a top-level span for the entire operation
    with tracer.start_as_current_span("observability_demo") as main_span:
        main_span.set_attribute("environment", "development")
        main_span.set_attribute("model", os.getenv("MODEL_NAME", "gpt-4o"))
        
        # Create agents
        with tracer.start_as_current_span("create_agents"):
            assistant = AssistantAgent(
                name="Assistant",
                model_client=model_client,
                system_message="You are a helpful assistant. Answer briefly and say DONE when finished.",
            )
        
        # Create team
        with tracer.start_as_current_span("create_team"):
            team = RoundRobinGroupChat(
                participants=[assistant],
                termination_condition=MaxMessageTermination(5),
            )
        
        # Run conversation with detailed tracing
        with tracer.start_as_current_span("run_conversation") as conv_span:
            conv_span.set_attribute("task", "greeting")
            
            print("Starting conversation with observability...\n")
            print("=" * 60)
            print("OpenTelemetry traces will be exported to console")
            print("=" * 60)
            print()
            
            result = await Console(
                team.run_stream(
                    task="Explain what observability means in software systems in 2 sentences."
                )
            )
            
            # Add result metrics to span
            conv_span.set_attribute("message_count", len(result.messages))
            conv_span.set_attribute("stop_reason", str(result.stop_reason))
            
            print(f"\n{'=' * 60}")
            print(f"Conversation Statistics:")
            print(f"{'=' * 60}")
            print(f"Messages exchanged: {len(result.messages)}")
            print(f"Stop reason: {result.stop_reason}")
            
            # Log each message for observability
            with tracer.start_as_current_span("process_results") as results_span:
                for i, msg in enumerate(result.messages):
                    with tracer.start_as_current_span(f"message_{i}") as msg_span:
                        msg_span.set_attribute("source", msg.source)
                        msg_span.set_attribute("message_length", len(str(msg.content)))
                        print(f"  [{i+1}] {msg.source}: {len(str(msg.content))} chars")
            
            print(f"{'=' * 60}")
            print("\n✓ Observability data captured via OpenTelemetry")
            print("  Check console output above for exported trace spans\n")


if __name__ == "__main__":
    asyncio.run(main())
