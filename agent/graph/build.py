from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from agent.graph.nodes import model_planner_node, route_planner, model_answer_node, tool_node
from agent.graph.state import AgentState
import sqlite3


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("plan", model_planner_node)
    graph.add_node("tool", tool_node)
    graph.add_node("answer", model_answer_node)
    
    graph.add_edge(START, "plan")
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
    
    conn = sqlite3.connect("checkpoints.db", check_same_thread=False)
    checkpointer = SqliteSaver(conn)
    
    return graph.compile(checkpointer=checkpointer)