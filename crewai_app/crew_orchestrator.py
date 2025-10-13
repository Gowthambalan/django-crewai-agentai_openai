import os
import yaml
from dotenv import load_dotenv
from crewai import Agent, Task, LLM
from .models import QueryLog  # ✅ Import model

# Load environment variables
load_dotenv()

AGENTS_FILE = os.path.join(os.path.dirname(__file__), "agents.yaml")
with open(AGENTS_FILE, "r") as f:
    agent_cfg = yaml.safe_load(f)

# Initialize LLM
openai_llm = LLM(model="gpt-4-turbo", api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Agents
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


def route_query(user_query: str):
    """Main routing logic with database logging."""
    
    # Create decision task
    decision_task = Task(
        description=f"""
        You are a decision-making AI agent.
        If the user query is related to cars, vehicles, or automotive topics,
        respond only with 'DataAgent'.
        Otherwise, respond only with 'WebAgent'.

        User query: "{user_query}"
        """,
        agent=decision_agent,
        expected_output="Either 'DataAgent' or 'WebAgent'"
    )
    
    # Execute decision task
    decision = decision_agent.execute_task(decision_task).strip()

    if "DataAgent" in decision:
        # Create data agent task
        data_task = Task(
            description=f"User Query: {user_query}",
            agent=data_agent,
            expected_output="A helpful response about automotive topics"
        )
        answer = data_agent.execute_task(data_task)
        routed_to = "DataAgent"
    else:
        # Create web agent task
        web_task = Task(
            description=f"User Query: {user_query}",
            agent=web_agent,
            expected_output="A helpful response to the general query"
        )
        answer = web_agent.execute_task(web_task)
        routed_to = "WebAgent"

    # ✅ Save query + response to PostgreSQL
    QueryLog.objects.create(
        user_query=user_query,
        decision=routed_to,
        response=answer
    )

    return {"decision": routed_to, "answer": answer}