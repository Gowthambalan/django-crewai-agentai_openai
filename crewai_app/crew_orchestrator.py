from crewai import Agent, Task, Crew, LLM
import os
import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load YAML config
AGENTS_FILE = os.path.join(os.path.dirname(__file__), "agents.yaml")
with open(AGENTS_FILE, "r") as f:
    agent_cfg = yaml.safe_load(f)

# LLM initialization
openai_llm = LLM(model="gpt-4-turbo", api_key=os.getenv("OPENAI_API_KEY"))

def route_query(user_query: str):
    """Main routing logic using CrewAI tasks."""
    
    # Define agents
    decision_agent = Agent(
        role=agent_cfg["DecisionAgent"]["role"],
        goal=agent_cfg["DecisionAgent"]["goal"],
        backstory=agent_cfg["DecisionAgent"]["backstory"],
        llm=openai_llm,
        verbose=True
    )

    data_agent = Agent(
        role=agent_cfg["DataAgent"]["role"],
        goal=agent_cfg["DataAgent"]["goal"],
        backstory=agent_cfg["DataAgent"]["backstory"],
        llm=openai_llm,
    )

    web_agent = Agent(
        role=agent_cfg["WebAgent"]["role"],
        goal=agent_cfg["WebAgent"]["goal"],
        backstory=agent_cfg["WebAgent"]["backstory"],
        llm=openai_llm,
    )

    # Decision task
    decision_task = Task(
        description=f"""
        Analyze the user query and decide which agent should handle it.
        If the query is about cars, vehicles, or automotive topics, choose 'DataAgent'.
        For all other queries, choose 'WebAgent'.
        
        User Query: "{user_query}"
        
        Respond with only one word: either 'DataAgent' or 'WebAgent'.
        """,
        agent=decision_agent,
        expected_output="Either 'DataAgent' or 'WebAgent'"
    )

    # Execute decision
    decision_crew = Crew(agents=[decision_agent], tasks=[decision_task])
    decision_result = decision_crew.kickoff()
    decision = str(decision_result).strip()

    # Route to appropriate agent
    if "DataAgent" in decision:
        data_task = Task(
            description=f"Provide a detailed and helpful response to this automotive-related query: {user_query}",
            agent=data_agent,
            expected_output="A comprehensive answer about cars, vehicles, or automotive topics"
        )
        data_crew = Crew(agents=[data_agent], tasks=[data_task])
        answer = data_crew.kickoff()
        routed_to = "DataAgent"
    else:
        web_task = Task(
            description=f"Provide a helpful response to this general query: {user_query}",
            agent=web_agent,
            expected_output="A helpful and informative response to the user's query"
        )
        web_crew = Crew(agents=[web_agent], tasks=[web_task])
        answer = web_crew.kickoff()
        routed_to = "WebAgent"

    return {"decision": routed_to, "answer": str(answer)}