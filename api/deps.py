from functools import lru_cache
from agent.graph.build import build_graph

@lru_cache()
def get_agent_graph():
    """
    Create and cache the agent graph instance for DI.
    """
    return build_graph()

# @lru_cache() 
# def get_redis_client():
#     return create_redis_client()