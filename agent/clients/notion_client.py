import os
import requests
from typing import Dict, Any, Optional

class NotionClient:
    """Notion API client for searching and retrieving page content."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("NOTION_API_KEY")
        if not self.api_key:
            raise ValueError("NOTION_API_KEY environment variable is required")

        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }

    # def search_pages(self, query: str) -> List[Dict[str, Any]]:
    #     """
    #     Search for pages in the Notion workspace.
        
    #     Args:
    #         query: Search query string
            
    #     Returns:
    #         List of search results with page information
            
    #     Raises:
    #         requests.RequestException: If API request fails
    #         ValueError: If query is invalid
    #     """
    

    def get_page_content(self, page_id: str) -> str:
        """
        Get full content of a specific page.
        
        Args:
            page_id: Notion page ID
            
        Returns:
            Formatted page content
        """
        if not page_id or not page_id.strip():
            raise ValueError("page_id cannot be empty")
            
        try:
            # Get page blocks
            url = f"{self.base_url}/blocks/{page_id}/children"
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            blocks = data.get("results", [])
            
            content_parts = []
            for block in blocks:
                block_content = self._extract_block_content(block)
                if block_content:
                    content_parts.append(block_content)
            
            return "\n".join(content_parts) if content_parts else "No content found"
            
        except requests.RequestException as e:
            return f"Error retrieving page content: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
    
    def _extract_block_content(self, block: Dict[str, Any]) -> str:
        """Extract text content from a block."""
        block_type = block.get("type", "")
        block_data = block.get(block_type, {})
        
        # Handle different block types
        if block_type in ["paragraph", "heading_1", "heading_2", "heading_3", 
                         "bulleted_list_item", "numbered_list_item"]:
            rich_text = block_data.get("rich_text", [])
            return "".join([text.get("plain_text", "") for text in rich_text])
        
        elif block_type == "code":
            rich_text = block_data.get("rich_text", [])
            code_text = "".join([text.get("plain_text", "") for text in rich_text])
            language = block_data.get("language", "")
            return f"```{language}\n{code_text}\n```"
        
        elif block_type == "quote":
            rich_text = block_data.get("rich_text", [])
            quote_text = "".join([text.get("plain_text", "") for text in rich_text])
            return f"> {quote_text}"
        
        return ""
    