"""Example of an agent with custom tools/functions using MAF."""
import asyncio
from typing import Annotated
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core.tools import FunctionTool
from config import get_model_client, get_tracer


# Define custom tools
def calculate_sum(a: Annotated[float, "First number"], 
                  b: Annotated[float, "Second number"]) -> float:
    """Calculate the sum of two numbers.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Sum of a and b
    """
    return a + b


def calculate_product(a: Annotated[float, "First number"], 
                      b: Annotated[float, "Second number"]) -> float:
    """Calculate the product of two numbers.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Product of a and b
    """
    return a * b


def get_weather(city: Annotated[str, "City name"]) -> str:
    """Get weather information for a city (mock function).
    
    Args:
        city: Name of the city
        
    Returns:
        Weather description
    """
    # This is a mock function - in real scenarios, you'd call a weather API
    weather_data = {
        "New York": "Sunny, 72°F",
        "London": "Cloudy, 15°C",
        "Tokyo": "Rainy, 20°C",
    }
    return weather_data.get(city, f"Weather data not available for {city}")


async def main():
    """Run an agent with custom tools."""
    
    # Get model client and tracer
    model_client = get_model_client()
    tracer = get_tracer()
    
    with tracer.start_as_current_span("agent_with_tools"):
        # Create tool instances
        tools = [
            FunctionTool(calculate_sum, description="Calculate the sum of two numbers"),
            FunctionTool(calculate_product, description="Calculate the product of two numbers"),
            FunctionTool(get_weather, description="Get weather information for a city"),
        ]
        
        # Create an assistant agent with custom tools
        assistant = AssistantAgent(
            name="MathWeatherAssistant",
            model_client=model_client,
            tools=tools,
            system_message="""You are a helpful assistant with access to math and weather tools.
            Use the available tools to help answer user questions. When all tasks are complete, say DONE.""",
        )
        
        # Create termination condition
        termination = MaxMessageTermination(10)
        
        # Create a team
        team = RoundRobinGroupChat(
            participants=[assistant],
            termination_condition=termination,
        )
        
        # Start conversation
        print("Starting agent with tools...\n")
        result = await Console(
            team.run_stream(
                task="""Please help me with the following:
                1. What is 15 + 27?
                2. What is 8 * 12?
                3. What's the weather like in Tokyo?"""
            )
        )
        
        print(f"\nTask completed. Messages exchanged: {len(result.messages)}")


if __name__ == "__main__":
    asyncio.run(main())
