from agents.graph.build import build_graph

def run_notion_agent():
    print("\n===== NOTION AGENT =====")

    app = build_graph()
    state = {"messages": []}
    
    for step in app.stream(state, stream_mode="values"):
        if "messages" in step:
            print_messages(step["messages"])
    
    print("\n ===== NOTION AGENT FINISHED =====")

def print_messages(messages):
    """Function to print the messages in a more readable format"""
    if not messages:
        return
    for message in messages:
        message_type = message.__class__.__name__.replace("Message", "").upper()
        print(f"\n{message_type}: {message.content}")

if __name__ == "__main__":
    run_notion_agent()

