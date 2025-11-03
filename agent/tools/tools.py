from langchain_core.tools import tool

@tool
def notion_tool() -> str:
    """Read user's Notion page content"""
    # TODO: implement actual Notion MCP or API call
    return """
    Tomorrow's meeting is at 10 AM.
    The project deadline is next Friday.
    I have a dentist appointment on Wednesday afternoon.
    Remember to buy groceries next weekend.
    """ 