import os
import shutil
from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.models.schemas import ResearchRequest, ResearchResponse, HealthResponse
from app.graph.research_graph import research_graph
from app.rag.pinecone_store import rag_service
from app.models.settings import settings

app = FastAPI(title="Multi-Agent Research Assistant")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.REPORT_DIR, exist_ok=True)

@app.post("/research", response_model=ResearchResponse)
async def conduct_research(request: ResearchRequest):
    # Execute the LangGraph
    initial_state = {
        "query": request.query,
        "search_results": [],
        "pdf_results": [],
        "summary": "",
        "citations": "",
        "final_report": "",
        "logs": ["Starting Research Automation..."]
    }
    
    final_state = await research_graph.ainvoke(initial_state)
    
    return {
        "query": request.query,
        "summary": final_state["summary"],
        "report": final_state["final_report"],
        "citations": final_state["citations"],
        "logs": final_state["logs"]
    }

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Process PDF into ChromaDB
    num_chunks = rag_service.process_pdf(file_path)
    
    return {"message": f"File {file.filename} uploaded and indexed.", "chunks": num_chunks}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return {"status": "healthy"}

# Serve Frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
