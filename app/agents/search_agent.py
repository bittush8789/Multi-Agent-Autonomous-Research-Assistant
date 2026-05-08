from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.tools import DuckDuckGoSearchRun
from app.models.settings import settings
from typing import List, Dict

class SearchAgent:
    def __init__(self):
        tavily_key = settings.TAVILY_API_KEY
        if tavily_key == "your_tavily_api_key_here":
            tavily_key = None
            
        self.tavily = None
        if tavily_key:
            import os
            os.environ["TAVILY_API_KEY"] = tavily_key
            try:
                self.tavily = TavilySearchResults(k=5)
            except Exception as e:
                print(f"Warning: Failed to initialize Tavily: {e}")
                
        self.ddg = DuckDuckGoSearchRun()

    def search(self, query: str) -> List[Dict]:
        results = []
        
        # Try Tavily first if API key is available
        if self.tavily:
            try:
                tavily_results = self.tavily.invoke(query)
                for res in tavily_results:
                    results.append({
                        "title": res.get("title", "Search Result"),
                        "content": res.get("content", ""),
                        "url": res.get("url", ""),
                        "source": "Tavily"
                    })
            except Exception as e:
                print(f"Tavily search failed: {e}")

        # Fallback or additional search with DuckDuckGo
        try:
            ddg_result = self.ddg.invoke(query)
            results.append({
                "title": "DuckDuckGo Summary",
                "content": ddg_result,
                "url": "https://duckduckgo.com",
                "source": "DuckDuckGo"
            })
        except Exception as e:
            print(f"DuckDuckGo search failed: {e}")

        return results

search_agent = SearchAgent()
