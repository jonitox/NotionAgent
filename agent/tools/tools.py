from langchain_core.tools import tool
from ..clients.notion_client import NotionClient
from ..clients.exceptions import NotionError

client = NotionClient()

@tool
def notion_tool() -> str:
    """
    Retrieve full content of a specific Notion page.
    
    Returns:
        Formatted page content.
    """
    page_id = "287cce4b-80c5-807d-8829-fd06c0556abe" # TODO: Example page ID; modify arguments to accept dynamic IDs.
    try:
        return client.get_page_content(page_id)
        
    except NotionError as e:
        return f"Error accessing Notion: {str(e)}"
    except Exception as e:
        return f"Unexpected error occurred: {str(e)}"