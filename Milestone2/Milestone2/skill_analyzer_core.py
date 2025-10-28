
import spacy
from spacy.matcher import PhraseMatcher
from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd
import re
from typing import List, Dict


try:
    
    nlp = spacy.load("en_core_web_sm")
except OSError:
    
    import spacy.cli
    print("Downloading spaCy model 'en_core_web_sm'...")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


sbert_model = SentenceTransformer('all-MiniLM-L6-v2')


SKILL_SET = [
    
    "Python", "SQL", "Machine Learning", "Data Analysis", "Project Management", 
    "TensorFlow", "Pytorch", "AWS", "Docker", "Tableau", "Full Stack Development",
    
    
    "Communication", "Leadership", "Critical Thinking", "Agile", "Scrum",
    
   
    "MS Office", "MS Visio", "Functional testing", "Business Analysis", 
    "Requirement documentation", "Documentation Skills", "Status Reporting", 
    "Coordination", "Requirements Gathering Tool"
]
TECH_KEYWORDS = [
    "Python", "SQL", "TensorFlow", "Pytorch", "AWS", "Docker", "Tableau",
    "MS Office", "MS Visio", "Functional testing", "Requirements Gathering Tool",
    "Machine Learning", "Data Analysis", "Full Stack Development"
]
SOFT_KEYWORDS = [
    "Management", "Communication", "Leadership", "Thinking", "Agile", "Scrum",
    "Documentation", "Status Reporting", "Coordination", "Business Analysis"
]

matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
patterns = [nlp.make_doc(skill.lower()) for skill in SKILL_SET]
matcher.add("Skill_Pattern", patterns)


def extract_skills_multi_method(text: str, source_type: str) -> List[Dict]:
    """
    Extracts skills using a combination of methods:
    1. PhraseMatcher (Dictionary-based/SpaCy)
    2. POS Tagging/Context (Identify Nouns near skill-related verbs)
    3. Custom NER (Placeholder for a trained model)
    """
    doc = nlp(text.lower())
    extracted_skills = set()
    matches = matcher(doc)
    for _, start, end in matches:
        skill = doc[start:end].text.title()
        extracted_skills.add(skill)
        
    
    for token in doc:
        
        if token.pos_ in ("NOUN", "PROPN") and token.i > 0 and doc[token.i - 1].pos_ in ('ADJ', 'NOUN'):
            phrase = f"{doc[token.i - 1].text.title()} {token.text.title()}"
            if any(kw.lower() in phrase.lower() for kw in SOFT_KEYWORDS):
                extracted_skills.add(phrase)
        
        
        if token.text in ('communication', 'leadership', 'adaptability', 'teamwork'):
            extracted_skills.add(token.text.title())


    
    final_list = []
    for skill in sorted(list(extracted_skills)):
        skill_type = "Technical" 
        
        
        if any(kw.lower() in skill.lower() for kw in TECH_KEYWORDS):
            skill_type = "Technical"
        
        elif any(kw.lower() in skill.lower() for kw in SOFT_KEYWORDS):
             skill_type = "Soft"
        elif skill in ["Management Skills", "Communication", "Decision Making", "Presentation"]:
             skill_type = "Soft"
             
        final_list.append({"skill": skill, "type": skill_type})
        
    return final_list


def get_skill_embeddings(skills: List[str]) -> np.ndarray:
    """Uses Sentence-BERT to generate embeddings for a list of skills."""
    if not skills:
        return np.array([])
    return sbert_model.encode(skills, convert_to_tensor=False)

def calculate_similarity_matrix(resume_skills: List[str], jd_skills: List[str]) -> pd.DataFrame:
    """
    Calculates the cosine similarity between every skill pair using BERT embeddings.
    """
    if not resume_skills or not jd_skills:
        return pd.DataFrame(index=resume_skills or [], columns=jd_skills or [])
    
   
    resume_embeddings = get_skill_embeddings(resume_skills)
    jd_embeddings = get_skill_embeddings(jd_skills)
    
    
    from sklearn.metrics.pairwise import cosine_similarity
    similarity_matrix = cosine_similarity(resume_embeddings, jd_embeddings)
    
   
    df = pd.DataFrame(
        similarity_matrix, 
        index=[f"R: {s}" for s in resume_skills], 
        columns=[f"JD: {s}" for s in jd_skills]
    )
    return df