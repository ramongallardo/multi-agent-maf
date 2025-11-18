"""Advanced example using SelectorGroupChat for dynamic agent selection."""
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.teams import SelectorGroupChat
from config import get_model_client, get_tracer


async def main():
    """Run a team with dynamic agent selection based on context."""
    
    # Get model client and tracer
    model_client = get_model_client()
    tracer = get_tracer()
    
    with tracer.start_as_current_span("selector_team"):
        # Create specialized agents
        data_analyst = AssistantAgent(
            name="DataAnalyst",
            model_client=model_client,
            system_message="""You are a data analyst expert. You specialize in:
            - Data analysis and statistics
            - Interpreting datasets and patterns
            - Creating data-driven insights
            Say PASS when you're done with your part.""",
            description="Expert in data analysis and statistics",
        )
        
        python_engineer = AssistantAgent(
            name="PythonEngineer",
            model_client=model_client,
            system_message="""You are a Python programming expert. You specialize in:
            - Writing clean, efficient Python code
            - Implementing algorithms and data structures
            - Code optimization and best practices
            Say PASS when you're done with your part.""",
            description="Expert in Python programming and software engineering",
        )
        
        ml_specialist = AssistantAgent(
            name="MLSpecialist",
            model_client=model_client,
            system_message="""You are a machine learning specialist. You specialize in:
            - Machine learning algorithms and models
            - Model training and evaluation
            - Feature engineering and selection
            Say DONE when the entire task is complete.""",
            description="Expert in machine learning and AI model development",
        )
        
        # Create a selector model client for choosing agents
        selector_client = get_model_client()
        
        # Create termination conditions
        termination = TextMentionTermination("DONE") | MaxMessageTermination(15)
        
        # Create a selector team - agents are selected dynamically based on context
        team = SelectorGroupChat(
            participants=[data_analyst, python_engineer, ml_specialist],
            model_client=selector_client,
            termination_condition=termination,
        )
        
        # Run the team with a complex task requiring multiple specialists
        print("Starting selector team collaboration...\n")
        result = await Console(
            team.run_stream(
                task="""We need to build a simple linear regression model. 
                
                Steps needed:
                1. Analyze what data we need for a basic example
                2. Write Python code to generate sample data (e.g., house prices based on size)
                3. Explain which ML algorithm to use and why
                
                Each specialist should contribute their expertise when needed."""
            )
        )
        
        print(f"\nTask completed!")
        print(f"Total messages: {len(result.messages)}")
        print(f"Stop reason: {result.stop_reason}")


if __name__ == "__main__":
    asyncio.run(main())
