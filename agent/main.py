from agent.graph.build import build_graph
from langchain_core.messages import AIMessage

def run_notion_agent_stream():
    print("\n===== NOTION AGENT =====")

    def print_messages(messages):
        """Function to print the messages in a more readable format"""
        if not messages:
            return
        print("\n===== MESSAGES =====")
        for message in messages:
            message_type = message.__class__.__name__
            print(
                f"\n{message_type}: {message.content}" +
                (f" (tool_call: {message.tool_calls[0]['name']})" if isinstance(message, AIMessage) and message.tool_calls else "")
                )

    app = build_graph()
    state = {"messages": []}
    
    for step in app.stream(state, stream_mode="values"):
        if "messages" in step:
            print_messages(step["messages"])
    
    print("\n ===== NOTION AGENT FINISHED =====")

if __name__ == "__main__":
    run_notion_agent_stream()

