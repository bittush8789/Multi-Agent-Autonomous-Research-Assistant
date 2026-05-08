from langchain_groq import ChatGroq
from app.models.settings import settings

def get_llm():
    if not settings.GROQ_API_KEY or settings.GROQ_API_KEY == "your_groq_api_key_here":
        raise ValueError("GROQ_API_KEY is not set. Please update your .env file with a valid API key.")
        
    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model_name=settings.MODEL_NAME,
        temperature=0.3
    )
