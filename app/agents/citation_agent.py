from typing import List, Dict

class CitationAgent:
    def format_citations(self, sources: List[Dict]) -> str:
        if not sources:
            return "No specific sources cited."
            
        citation_list = []
        for i, source in enumerate(sources, 1):
            title = source.get("title", "Untitled")
            url = source.get("url", "N/A")
            origin = source.get("source", "Unknown")
            citation_list.append(f"[{i}] {title} - {origin} (Link: {url})")
            
        return "\n".join(citation_list)

citation_agent = CitationAgent()
