from langchain_core.tools import tool

@tool
def notion_tool() -> str:
    """Read user's Notion page content"""
    # TODO: implement actual Notion MCP or API call
    return "I know about Notion pages!" 