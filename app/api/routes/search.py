from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.candidate import Candidate
from app.schemas.search import SearchRequest, SearchResponse, CandidateResponse
from app.services.jd_parser import JDParserService
from app.services.ranking_engine import RankingEngine

router = APIRouter(prefix="/api/v1/search", tags=["search"])

@router.post("/", response_model=SearchResponse)
def search_candidates(request: SearchRequest, db: Session = Depends(get_db)):
    # 1. Parse JD
    parser = JDParserService()
    requirements = parser.parse(request.job_description)
    
    # 2. Get all candidates (In production, use filters here)
    candidates = db.query(Candidate).all()
    
    # 3. Rank them
    ranker = RankingEngine()
    scored_candidates = []
    
    for c in candidates:
        result = ranker.calculate_score(c, requirements)
        if result["total_score"] > 0: # Only return if there's some match
            scored_candidates.append({
                "candidate": c,
                "score": result["total_score"],
                "details": result
            })
            
    # Sort by score descending
    scored_candidates.sort(key=lambda x: x["score"], reverse=True)
    
    # Format response
    final_list = []
    for item in scored_candidates[:request.limit]:
        c = item["candidate"]
        final_list.append(CandidateResponse(
            id=c.id,
            full_name=c.full_name,
            email=c.email,
            university=c.university,
            major=c.major,
            graduation_year=c.graduation_year,
            professional_skills=c.professional_skills,
            match_score=item["score"],
            matched_skills=item["details"]["matched_skills"],
            missing_skills=item["details"]["missing_skills"],
            explanation=item["details"]["explanation"]
        ))
        
    return SearchResponse(
        query=request.job_description,
        total_results=len(final_list),
        candidates=final_list
    )