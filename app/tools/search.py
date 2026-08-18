from langchain_core.tools import tool
from duckduckgo_search import DDGS

@tool
async def search_web(query: str) -> str:
    """Useful for searching the web for current events, news, and real-time facts.
    Input should be a concise search query string.
    """
    try:
        # Perform asynchronous web search using DuckDuckGo
        results = []
        with DDGS() as ddgs:
            search_results = list(ddgs.text(query, max_results=3))
            
            if not search_results:
                return f"No relevant web search results found for: {query}"
            
            for res in search_results:
                title = res.get("title", "No Title")
                snippet = res.get("body", "No Snippet")
                url = res.get("href", "")
                results.append(f"Title: {title}\nSnippet: {snippet}\nURL: {url}\n---")
                
        return "\n".join(results)
        
    except Exception as e:
        return f"Error executing web search: {str(e)}"