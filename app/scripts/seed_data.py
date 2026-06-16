import sys
import os
import pandas as pd

# 1. Get the directory of this script (app/scripts)
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Go up TWO levels to reach the project root (PromptToFilter)
# Level 1: app/scripts -> app
# Level 2: app -> PromptToFilter
project_root = os.path.dirname(os.path.dirname(current_dir))

# 3. Add project root to system path so we can import 'app' modules
sys.path.append(project_root)

# 4. Change working directory to the root so relative paths work
os.chdir(project_root)

from app.database import SessionLocal, engine, Base
from app.models.candidate import Candidate

def seed_data():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    
    # 5. Construct the exact path to the CSV file
    csv_path = os.path.join(project_root, "data", "students.csv")
    
    if not os.path.exists(csv_path):
        print(f"❌ Error: Could not find {csv_path}")
        print("Please make sure 'students.csv' is inside the 'data' folder.")
        return

    print(f"✅ Reading CSV from {csv_path}...")
    try:
        # Read CSV
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return
    
    db = SessionLocal()
    
    count = 0
    print("Inserting candidates into database...")
    for index, row in df.iterrows():
        # Helper functions to handle missing data safely
        def get_str(val):
            return str(val).strip() if pd.notna(val) else ""
        
        def get_float(val, default=0.0):
            try:
                return float(val) if pd.notna(val) else default
            except:
                return default
                
        def get_int(val, default=2025):
            try:
                return int(float(val)) if pd.notna(val) else default
            except:
                return default

        # Map CSV columns to Database Model
        skills = get_str(row.get("skills_professional_skills"))
        aptitude = get_float(row.get("intelligence_assessment_scores_aptitude"))
        coding = get_float(row.get("intelligence_assessment_scores_coding"))
        grad_year = get_int(row.get("graduation_year"))
        
        candidate = Candidate(
            full_name=get_str(row.get("full_name")),
            email=get_str(row.get("email")) or f"student_{index}@test.com",
            university=get_str(row.get("university")),
            major=get_str(row.get("major")),
            graduation_year=grad_year,
            current_location=get_str(row.get("current_location")),
            professional_skills=skills,
            projects=get_str(row.get("skills_projects")),
            certifications=get_str(row.get("skills_certifications")),
            aptitude_score=aptitude,
            coding_score=coding,
            gpa_proxy=(aptitude + coding) / 2
        )
        
        db.add(candidate)
        count += 1
        
    db.commit()
    print(f"🎉 Successfully seeded {count} candidates into the database!")
    db.close()

if __name__ == "__main__":
    seed_data()