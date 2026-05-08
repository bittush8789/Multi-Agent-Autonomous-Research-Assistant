from typing import TypedDict, List, Dict, Annotated
import operator
from langgraph.graph import StateGraph, END
from app.agents.search_agent import search_agent
from app.agents.summarizer_agent import summarizer_agent
from app.agents.citation_agent import citation_agent
from app.agents.report_agent import report_agent
from app.rag.pinecone_store import rag_service

class AgentState(TypedDict):
    query: str
    search_results: List[Dict]
    pdf_results: List[str]
    summary: str
    citations: str
    final_report: str
    logs: Annotated[List[str], operator.add]

def search_node(state: AgentState):
    query = state["query"]
    results = search_agent.search(query)
    return {
        "search_results": results,
        "logs": [f"Search Agent: Found {len(results)} sources."]
    }

def pdf_node(state: AgentState):
    query = state["query"]
    results = rag_service.search(query)
    pdf_texts = [res.page_content for res in results]
    return {
        "pdf_results": pdf_texts,
        "logs": [f"PDF Agent: Extracted {len(pdf_texts)} relevant segments from internal docs."]
    }

def summarize_node(state: AgentState):
    summary = summarizer_agent.summarize(state["search_results"], "\n".join(state["pdf_results"]))
    return {
        "summary": summary,
        "logs": ["Summarizer Agent: Condensed all research findings."]
    }

def citation_node(state: AgentState):
    citations = citation_agent.format_citations(state["search_results"])
    return {
        "citations": citations,
        "logs": ["Citation Agent: Formatted references and links."]
    }

def report_node(state: AgentState):
    report = report_agent.generate_report(state["summary"], state["citations"])
    return {
        "final_report": report,
        "logs": ["Report Agent: Finalized structured research report."]
    }

# Build Graph
builder = StateGraph(AgentState)

builder.add_node("search", search_node)
builder.add_node("pdf_search", pdf_node)
builder.add_node("summarize", summarize_node)
builder.add_node("citation", citation_node)
builder.add_node("report", report_node)

builder.set_entry_point("search")
builder.add_edge("search", "pdf_search")
builder.add_edge("pdf_search", "summarize")
builder.add_edge("summarize", "citation")
builder.add_edge("citation", "report")
builder.add_edge("report", END)

research_graph = builder.compile()
