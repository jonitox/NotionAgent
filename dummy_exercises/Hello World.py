
from typing import TypedDict
from langgraph.graph import StateGraph

class MyState(TypedDict):
    a: int
    b: str


def greeting_node(state: MyState) -> MyState:
    """This is a greeting node."""
    state['a'] += 1
    state['b'] = f"Hello, the value of a is {state['a']}"
    state['c'] = "This is an added field."
    return state

graph = StateGraph(MyState)
graph.add_node("greeter", greeting_node)

graph.set_entry_point("greeter")
graph.set_finish_point("greeter")

app = graph.compile()
print(app.invoke({"a": 1, "b": "yoyo"}))

from IPython.display import Image, display
display(Image(app.get_graph().draw_mermaid_png()))