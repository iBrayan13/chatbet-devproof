import uuid
import traceback

from langgraph.prebuilt  import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import HumanMessage, SystemMessage

from src.agent.agent_config import agent_llm, system_prompt, agent_tools

agent_node = create_react_agent(agent_llm, agent_tools)
workflow = StateGraph(state_schema=MessagesState)
workflow.add_edge(START, "model")
workflow.add_node("model", agent_node)


memory = MemorySaver()
app = workflow.compile(
    checkpointer=memory
)
config = {"configurable": {"thread_id": uuid.uuid4()}}

def get_agent_response(user_input: str) -> str:
    try:
        return app.invoke(
            input={"messages": [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_input)
            ]},
            config=config
        )["messages"][-1].content
    
    except:
        traceback.print_exc()
        return "Something went wrong. Please try again."