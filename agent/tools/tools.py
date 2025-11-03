from langchain_core.tools import tool
from ..clients.notion_client import NotionClient

client = NotionClient()

# @tool
# def notion_tool(query: str = "") -> str:
#     """
#     Search and retrieve content from user's Notion pages.
#
#     Args:
#         query: Search query to find relevant pages. If empty, returns general info.
    
#     Returns:
#         Formatted search results or page content from Notion.
#     """
#     try:
#         if query.strip():
#             return client.search_pages(query)
#         else:
#             return "Please provide a search query to find relevant Notion pages."
            
#     except ValueError as e:
#         return f"Configuration error: {str(e)}"
#     except Exception as e:
#         return f"Error accessing Notion: {str(e)}"
    
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
        
    except ValueError as e:
        return f"Configuration error: {str(e)}"
    except Exception as e:
        return f"Error retrieving page content: {str(e)}"