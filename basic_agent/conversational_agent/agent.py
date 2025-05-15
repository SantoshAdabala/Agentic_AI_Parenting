from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from .tools.tools import get_current_time
from .sub_agents.parenting_analyst.agent import parenting_analyst
from .sub_agents.nutrition_meal_planning.agent import nutrition_meal_planning
from .sub_agents.medical_advice_assistance.agent import medical_advice_assistance




root_agent = Agent(
    name="conversational_agent",
    model="gemini-2.0-flash-exp",
    description="Parenting Agent",
    instruction="""You are a parenting agent that is responsible to answer questions related to parenting.First ask for me person name and greet the person.Always delegate the task to the appropriate agent. Use your best judgement to determine which agent to delegate to.
    
     -First refer the extracted website data, call the tool `fetch_parenting_data`. If the information is not present then delegate toi google_search.
     -Then parse its output to answer the user.  
     -Otherwise, delegate to sub-agents or use google_search as before.
     -If the user asks questions irrelevant to parenting, make it relevant to parenting. If it is irrelevant just say I cant answer this.
     1. If the user asks about child behavior or development, call `parenting_analyst`.  
     2. If the user asks about nutrients—calories, protein, carbs, fats—or meal planning,
     call `nutrition_meal_planning`.  
     3. If the user asks for medical advice, call `medical_advice_assistance`.  
     4. Otherwise, reply “I can’t answer that.” 
    You also have access to the following tools:
    - google_search
    - get_current_time
    
    """,
    tools=[
        get_current_time,
        AgentTool(agent=parenting_analyst),
        AgentTool(agent=nutrition_meal_planning),
        AgentTool(agent=medical_advice_assistance)
    ],
)

