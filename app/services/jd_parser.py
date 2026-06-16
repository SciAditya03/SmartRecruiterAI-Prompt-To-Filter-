import re
from typing import List, Dict

class JDParserService:
    def parse(self, text: str) -> Dict:
        text_lower = text.lower()
        
        # Extract Skills (Simple keyword matching for MVP)
        common_skills = [
            "python", "java", "c++", "react", "node.js", "sql", "machine learning", 
            "ml", "ai", "data science", "aws", "docker", "kubernetes", "pytorch", 
            "tensorflow", "html", "css", "javascript", "typescript", "figma"
        ]
        
        found_skills = []
        for skill in common_skills:
            if skill in text_lower:
                found_skills.append(skill)
                
        # Extract Graduation Year (e.g., "2025", "2026")
        year_match = re.search(r'(202[4-9]|2030)', text)
        grad_year = int(year_match.group(0)) if year_match else None
        
        # Extract GPA requirement (e.g., "8.0", "above 8")
        gpa_match = re.search(r'(?:gpa|cgpa).?(\d+\.?\d*)', text_lower)
        min_gpa = float(gpa_match.group(1)) if gpa_match else 0.0

        return {
            "skills": found_skills,
            "graduation_year": grad_year,
            "min_gpa": min_gpa,
            "raw_text": text
        }