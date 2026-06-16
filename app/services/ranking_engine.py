from typing import List, Dict
import math

class RankingEngine:
    def calculate_score(self, candidate, job_requirements: Dict) -> Dict:
        candidate_skills = set(candidate.professional_skills.lower().split('|')) if candidate.professional_skills else set()
        # Clean up skills (remove spaces)
        candidate_skills = {s.strip() for s in candidate_skills}
        
        required_skills = set(job_requirements.get("skills", []))
        
        # 1. Skill Match (60% weight)
        matched = candidate_skills.intersection(required_skills)
        missing = required_skills - candidate_skills
        
        skill_score = 0
        if len(required_skills) > 0:
            skill_score = (len(matched) / len(required_skills)) * 60
            
        # 2. Graduation Year Match (20% weight)
        year_score = 0
        if job_requirements.get("graduation_year"):
            if candidate.graduation_year == job_requirements["graduation_year"]:
                year_score = 20
            elif abs(candidate.graduation_year - job_requirements["graduation_year"]) == 1:
                year_score = 10
                
        # 3. Assessment/GPA Proxy (20% weight)
        # Using average of aptitude and coding scores from dataset
        avg_score = 0
        if candidate.aptitude_score and candidate.coding_score:
            avg_score = (candidate.aptitude_score + candidate.coding_score) / 2
        # Normalize 0-100 scale to 0-20 points
        assessment_score = (avg_score / 100) * 20
        
        total_score = skill_score + year_score + assessment_score
        
        return {
            "total_score": round(total_score, 2),
            "matched_skills": list(matched),
            "missing_skills": list(missing),
            "explanation": f"Matched {len(matched)}/{len(required_skills)} skills. Year: {candidate.graduation_year}. Avg Score: {avg_score:.1f}"
        }