import asyncio
from langchain_core.tools import tool
from duckduckgo_search import DDGS


def _fetch_ddg_results(query: str, max_results: int = 3) -> list:
    """Synchronous helper function to interact with DDGS."""
    with DDGS() as ddgs:
        return list(ddgs.text(query, max_results=max_results))


@tool
async def search_web(query: str) -> str:
    """Useful for searching the web for current events, news, and real-time facts.
    Input should be a concise search query string.
    """
    try:
        # Offload synchronous DDGS call to a separate thread to keep the event loop non-blocking
        search_results = await asyncio.to_thread(_fetch_ddg_results, query, 3)

        if not search_results:
            return f"No relevant search results found for: '{query}'. Do not re-search; synthesize your final report now."

        results = []
        for res in search_results:
            title = res.get("title", "No Title")
            snippet = res.get("body", "No Snippet")
            url = res.get("href", "")
            results.append(f"Title: {title}\nSnippet: {snippet}\nURL: {url}\n---")

        return "\n".join(results)

    except Exception as e:
        return f"Error executing web search: {str(e)}. Proceed with existing knowledge and finish the response."