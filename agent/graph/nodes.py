from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
from agent.graph.state import AgentState
from agent.tools.tools import notion_tool

load_dotenv() # TODO: modify .env loading

# TODO: enable model selection
planner_model = ChatOpenAI(model="gpt-4o-mini").bind_tools([notion_tool]) # model for planning execution
answer_model = ChatOpenAI(model="gpt-4o").bind_tools([notion_tool]) # model for final answer generation
MAX_TURNS = 10

def ingest_node(state: AgentState) -> AgentState:
    input_message = HumanMessage(content=input("Enter your message: "))
    return {"messages": state["messages"] + [input_message]}

def model_planner_node(state: AgentState) -> AgentState:
    """Plan execution strategy based on user request."""    
    system_prompt = SystemMessage(content="""
    You are a planning agent. Analyze the user's request and decide ONLY whether to call tools.
    
    - If a Notion lookup is needed, RETURN a tool call.
    - If not, DO NOT answer; produce no content.
    """)
    
    response = planner_model.invoke([system_prompt] + state["messages"])
    
    if getattr(response, "tool_calls", None): 
        return {"messages": state["messages"] + [response]}
    return {"messages": state["messages"]}

def route_planner(state: AgentState):
    """Route based on whether tools were called."""
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage) and getattr(last_message, "tool_calls", None):
        return "tool"
    return "answer"

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

    pruned = [m for m in state["messages"] if not isinstance(m, ToolMessage)]
    pruned = pruned[-MAX_TURNS*2:]

    return {"messages": pruned + [response]}

tool_node = ToolNode([notion_tool])