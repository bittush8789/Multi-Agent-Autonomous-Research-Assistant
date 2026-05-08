from app.services.llm_factory import get_llm
from langchain_core.prompts import ChatPromptTemplate
from typing import List, Dict

class SummarizerAgent:
    def __init__(self):
        self.llm = get_llm()
        self.prompt = ChatPromptTemplate.from_template("""
        You are an expert Research Summarizer. Your goal is to condense the following information into key insights.
        
        Information:
        {content}
        
        Provide a structured summary including:
        - Executive Summary
        - Key Trends
        - Technical Insights
        - Potential Challenges
        """)

    def summarize(self, search_results: List[Dict], pdf_content: str = "") -> str:
        combined_content = ""
        for res in search_results:
            combined_content += f"Source: {res['source']} - {res['title']}\nContent: {res['content']}\n\n"
        
        if pdf_content:
            combined_content += f"PDF Content:\n{pdf_content}\n"

        chain = self.prompt | self.llm
        response = chain.invoke({"content": combined_content})
        return response.content

summarizer_agent = SummarizerAgent()
