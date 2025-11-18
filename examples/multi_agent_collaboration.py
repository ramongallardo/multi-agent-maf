"""Multi-agent collaboration example with researcher and writer agents using MAF."""
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from config import get_model_client, get_tracer


async def main():
    """Run a multi-agent collaboration for research and writing."""
    
    # Get model client and tracer
    model_client = get_model_client()
    tracer = get_tracer()
    
    with tracer.start_as_current_span("multi_agent_collaboration"):
        # Create a researcher agent
        researcher = AssistantAgent(
            name="Researcher",
            model_client=model_client,
            system_message="""You are a research specialist. Your role is to:
            1. Gather and analyze information on given topics
            2. Provide factual, well-researched insights
            3. Cite your reasoning clearly
            You work with the Writer to create comprehensive content.""",
        )
        
        # Create a writer agent
        writer = AssistantAgent(
            name="Writer",
            model_client=model_client,
            system_message="""You are a professional writer. Your role is to:
            1. Transform research into engaging, well-structured content
            2. Ensure clarity and readability
            3. Create compelling narratives from factual information
            You work with the Researcher to produce high-quality articles.""",
        )
        
        # Create a critic agent for quality control
        critic = AssistantAgent(
            name="Critic",
            model_client=model_client,
            system_message="""You are a content critic. Your role is to:
            1. Review the work produced by the Researcher and Writer
            2. Provide constructive feedback
            3. Ensure accuracy, clarity, and quality
            When the content meets high standards, respond with TERMINATE.""",
        )
        
        # Create termination conditions
        termination = TextMentionTermination("TERMINATE") | MaxMessageTermination(20)
        
        # Create a round-robin team for collaboration
        team = RoundRobinGroupChat(
            participants=[researcher, writer, critic],
            termination_condition=termination,
        )
        
        # Start the collaboration
        print("Starting multi-agent collaboration...\n")
        result = await Console(
            team.run_stream(
                task="""Create a brief article (2-3 paragraphs) about the benefits of 
                multi-agent systems in artificial intelligence. The Researcher should gather 
                key points, the Writer should create the article, and the Critic should review it."""
            )
        )
        
        print(f"\nCollaboration completed. Total messages: {len(result.messages)}")
        print(f"Stop reason: {result.stop_reason}")


if __name__ == "__main__":
    asyncio.run(main())
