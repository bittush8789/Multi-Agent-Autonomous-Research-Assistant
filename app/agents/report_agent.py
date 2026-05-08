from app.services.llm_factory import get_llm
from langchain_core.prompts import ChatPromptTemplate

class ReportAgent:
    def __init__(self):
        self.llm = get_llm()
        self.prompt = ChatPromptTemplate.from_template("""
        You are a Senior Research Analyst. Create a professional, structured research report based on the summary and citations provided.
        
        Summary:
        {summary}
        
        Citations:
        {citations}
        
        The report should follow this structure:
        1. Introduction
        2. Current Trends
        3. Tools & Technologies
        4. Architecture & Implementation
        5. Industry Use Cases
        6. Challenges & Future Scope
        7. Recommendations
        8. References
        
        Format the output in high-quality Markdown.
        """)

    def generate_report(self, summary: str, citations: str) -> str:
        chain = self.prompt | self.llm
        response = chain.invoke({"summary": summary, "citations": citations})
        return response.content

report_agent = ReportAgent()
