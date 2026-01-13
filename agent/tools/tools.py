from langchain_core.tools import tool
from functools import lru_cache
from ..clients.notion_client import NotionClient
from ..clients.exceptions import NotionError
from agent.settings import settings
from agent.graph.state import AgentState


@lru_cache(maxsize=128)
def get_notion_client(api_key: str) -> NotionClient:
    """Get or create cached NotionClient instance."""
    return NotionClient(api_key=api_key)


def create_notion_tool(state: AgentState):
    """Create a notion tool with user's API key and page ID from state."""
    
    notion_api_key = state.get("notion_api_key")
    if not notion_api_key:
        raise ValueError("Notion API key not configured in user settings")
    
    notion_page_id = state.get("notion_page_id")
    if not notion_page_id:
        raise ValueError("Notion page ID not configured in user settings")
    
    # Use cached client
    client = get_notion_client(notion_api_key)
    
    @tool
    def notion_tool() -> str:
        """
        Retrieve full content of a specific Notion page.
        
        Returns:
            Formatted page content.
        """
        if not notion_page_id:
            return "Error: Notion page ID not configured in user settings"
        
        try:
            return client.get_page_content(notion_page_id)
            
        except NotionError as e:
            return f"Error accessing Notion: {str(e)}"
        except Exception as e:
            return f"Unexpected error occurred: {str(e)}"
    
    return notion_tool