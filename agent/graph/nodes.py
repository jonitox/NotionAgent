from typing import List
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from langchain_core.messages import AIMessage, ToolMessage, SystemMessage, RemoveMessage
from agent.graph.state import AgentState
from agent.tools.tools import notion_tool
from agent.settings import settings

# TODO: enable model selection
planner_model = ChatOpenAI(
    model=settings.OPENAI_MODEL_PLANNER,
    api_key=settings.OPENAI_API_KEY
).bind_tools([notion_tool])
answer_model = ChatOpenAI(
    model=settings.OPENAI_MODEL_ANSWER,
    api_key=settings.OPENAI_API_KEY
).bind_tools([notion_tool])

def model_planner_node(state: AgentState) -> AgentState: 
    """Plan execution strategy based on user request."""    
    system_prompt = SystemMessage(content="""
    You are a planning agent. Analyze the user's request and decide ONLY whether to call tools.
    
    - If a Notion lookup is needed, RETURN a tool call.
    - If not, DO NOT answer; produce no content.
    """)
    
    response = planner_model.invoke([system_prompt] + state["messages"])

    if getattr(response, "tool_calls", None): 
        return {"messages": [response]}
    return {"messages": []}

def route_planner(state: AgentState):
    """Route based on whether tools were called."""
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and getattr(last_message, "tool_calls", None):
        return "tool"
    return "answer"

def clean_up(state: AgentState) -> List[str]:
    """Collect message ids to drop: tool outputs, planner tool_calls, and old turns."""
    removable_ids = []
    
    # Drop ToolMessage and planner AIMessage with tool_calls
    for m in state["messages"]:
        if isinstance(m, ToolMessage) or (isinstance(m, AIMessage) and getattr(m, "tool_calls", None)):
            removable_ids.append(m.id)

    # Keep only MAX_TURNS (Human + AI = 1 turn); subtract 1 to account for the response appended after cleanup.
    keep_count = settings.MAX_TURNS * 2 - 1 
    
    remaining = [m for m in state["messages"] if m.id not in set(removable_ids)]
    if len(remaining) > keep_count:
        removable_ids.extend([m.id for m in remaining[: -(keep_count)]])

    return removable_ids

def model_answer_node(state: AgentState) -> AgentState:
    """Generate final user-facing response based on all available context."""

    has_tool_result = isinstance(state["messages"][-1], ToolMessage)
    if has_tool_result:
        system_prompt = SystemMessage(content="""
        You are a helpful assistant. Based on the tool results and conversation history,
        provide a comprehensive, well-structured answer to the user's question.
        
        Use the information from the Notion search results to give accurate and detailed responses.
        If the tool results are insufficient, acknowledge this and provide what information you can.
        """)
    else:
        system_prompt = SystemMessage(content="""
        You are a helpful assistant. Provide a direct, informative, and engaging response
        to the user's question based on your knowledge and the conversation context.
        """)
    response = answer_model.invoke([system_prompt] + state["messages"])
    
    remove_ids = clean_up(state)
    
    return {"messages": [RemoveMessage(id=i) for i in remove_ids] + [response]}

tool_node = ToolNode([notion_tool])