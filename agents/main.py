from dotenv import load_dotenv  
from agents.tools.tools import notion_tool

load_dotenv() # TODO: .env 변경?

tools = [notion_tool]
model = ChatOpenAI(model = "gpt-4o").bind_tools(tools)

def run_notion_agent():
    print("\n===== NOTION AGENT =====")

if __name__ == "__main__":
    run_notion_agent()