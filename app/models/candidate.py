from sqlalchemy import Column, Integer, String, Float, Text, JSON
from app.database import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    university = Column(String)
    major = Column(String)
    graduation_year = Column(Integer)
    current_location = Column(String)
    
    # Skills stored as a comma-separated string or JSON
    professional_skills = Column(Text) 
    projects = Column(Text)
    certifications = Column(Text)
    
    # Assessment scores
    aptitude_score = Column(Float)
    coding_score = Column(Float)
    gpa_proxy = Column(Float) # Using aptitude/coding avg as proxy if GPA missing

    # Raw data for search
    raw_data = Column(JSON) 