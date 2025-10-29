from langgraph.graph import StateGraph
from agents.graph.state import AgentState

def build_graph():
    graph = StateGraph(AgentState)
    return graph.compile()