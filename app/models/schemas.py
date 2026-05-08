from pydantic import BaseModel
from typing import List, Optional

class ResearchRequest(BaseModel):
    query: str

class ResearchResponse(BaseModel):
    query: str
    summary: str
    report: str
    citations: str
    logs: List[str]

class HealthResponse(BaseModel):
    status: str
