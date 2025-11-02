from langgraph.graph import StateGraph, START, END
from agents.graph.nodes import ingest_node, model_planner_node, route_planner, tool_node, model_answer_node
from agents.graph.state import AgentState

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("ingest", ingest_node)
    graph.add_node("plan", model_planner_node)
    graph.add_node("tool", tool_node)
    graph.add_node("answer", model_answer_node)
    
    
    graph.add_edge(START, "ingest")
    graph.add_edge("ingest", "plan")
    graph.add_conditional_edges(
        "plan",
        route_planner,
        {
            "tool": "tool",
            "answer": "answer",
        }
    )
    graph.add_edge("tool", "answer")
    graph.add_edge("answer", END)

    
    return graph.compile()