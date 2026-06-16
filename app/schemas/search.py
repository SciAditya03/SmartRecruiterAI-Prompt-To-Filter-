from pydantic import BaseModel
from typing import List, Optional, Dict

class SearchRequest(BaseModel):
    job_description: str
    limit: int = 10

class CandidateResponse(BaseModel):
    id: int
    full_name: str
    email: str
    university: str
    major: str
    graduation_year: int
    professional_skills: str
    match_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    explanation: str

    class Config:
        from_attributes = True

class SearchResponse(BaseModel):
    query: str
    total_results: int
    candidates: List[CandidateResponse]