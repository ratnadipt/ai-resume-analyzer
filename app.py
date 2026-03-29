# 1. Import required dependency.
import streamlit as st
import pdfplumber
import re
import nltk
from nltk.corpus import stopwords

# ------------------------------------------------------
# Download stopwords -> only Once
nltk.download("stopwords")
# ------------------------------------------------------

# ------------------------------------------------------
# DEFINE JOB ROLES
JOB_ROLES = {
  "Web Developer": ["html", "css", "javascript", "react", "angular", "node", "nodejs", "mysql", "mongodb", "tailwind", "bootstrap"],
  "Java Developer": ["java", "spring", "spring boot", "hibernate", "jdbc", "sql", "oops"],
  "Data Scientist": ["python", "machine learning", "pandas", "numpy", "sql", "statistics"]
}
# ------------------------------------------------------

# ------------------------------------------------------
# TEXT EXTRACTIONS FROM PDF
def extract_text_from_pdf(file):
  text = ""
  with pdfplumber.open(file) as pdf:
    for page in pdf.pages:
      text += page.extract_text() or ""
  
  return text.lower()
# ------------------------------------------------------

# ------------------------------------------------------
# TEXT PREPROCESSING
stop_words = set(stopwords.words('english'))
def proprocess_text(text): 
  text = re.sub("r[^a-zA-Z ]", "", text)
  words = text.lower().split()
  words = [w for w in words if w not in stop_words]
  return words
# ------------------------------------------------------

# ------------------------------------------------------
# SKILL MATHING
def extract_skill(text, required_skills):
  found_skills = []
  for skill in required_skills:
    if skill.lower() in text:
      found_skills.append(skill)
  return found_skills
# ------------------------------------------------------
# CALCULATE SCORE MODULE
def calculate_score(found_skills, required_skills):
  if len(required_skills) == 0:
    return 0
  score = int((len(found_skills) / len(required_skills))* 100)
  return score
# ------------------------------------------------------

# ------------------------------------------------------
# INDENTIFY MISSING SKILLS
def get_missing_skills(found_skills, required_skills):
  return list(set(required_skills) - set(found_skills))
# ------------------------------------------------------

# ------------------------------------------------------
# STREAMLIT DASHBOARD UI
# ------------------------------------------------------
st.set_page_config(page_title="AI Resume Analyzer", layout="centered")
st.title("AI Resume Analyzer")
st.markdown("### Upload your resume and check Job Role.")

uploaded_file = st.file_uploader("Upload Resume (Only PDF)", type=['pdf'])
job_role = st.selectbox("Select Job Role", list(JOB_ROLES.keys()))

# MAIN LOGIC
if uploaded_file is not None:
  # Extract
  text = extract_text_from_pdf(uploaded_file)

  # Pre Process
  words = proprocess_text(text)

  # Required skill
  required_skills = JOB_ROLES[job_role]

  # Extract matched Skills
  found_skills = extract_skill(text, required_skills)

  # Calculate Score
  score = calculate_score(found_skills, required_skills)

  # Missing skills
  missing_skills = get_missing_skills(found_skills, required_skills)

# --------------------------------------------------
# OUTPUT 
st.subheader("Resume Score")
st.progress(score)
st.success(f"Match Score: {score}/100")

st.subheader("Skills Found")
if found_skills:
  st.write(", ".join(found_skills))
else:
  st.warning("No Relevant skills found.")

st.subheader("Missing Skills")
if missing_skills:
  st.write(", ".join(missing_skills))
else:
  st.success("No Missing Skills, Good Resume!")

st.subheader("Suggestions")
if missing_skills:
  st.info("Add these skills to improve your resume:")
  for skill in missing_skills:
    st.write(f"Add: {skill}")
else:
  st.success("Your resume is well aligned with the job role!")
# --------------------------------------------------
