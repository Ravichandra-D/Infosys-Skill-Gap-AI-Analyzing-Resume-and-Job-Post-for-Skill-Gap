import spacy
import re

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Example Skill Database
SKILL_DATABASE = {
    'programming_languages': ['Python', 'Java', 'C', 'C++', 'C#', 'JavaScript', 'R', 'Go', 'Ruby', 'PHP'],
    'frameworks': ['TensorFlow', 'PyTorch', 'Scikit-learn', 'Keras', 'React', 'Angular', 'Django', 'Flask', 'Spring', 'Node.js'],
    'databases': ['MySQL', 'PostgreSQL', 'MongoDB', 'SQLite', 'Oracle'],
    'cloud': ['AWS', 'Azure', 'Google Cloud', 'IBM Cloud', 'Heroku'],
    'soft_skills': ['Leadership', 'Teamwork', 'Communication', 'Problem-solving', 'Time Management', 'Analytical']
}


# Method 1: Keyword matching from database
def keyword_match(text, skill_database):
    found = []
    text_lower = text.lower()
    for category, skills in skill_database.items():
        for skill in skills:
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found.append(skill)
    return found


# Method 2: POS Pattern Matching (ADJ+NOUN, NOUN+NOUN)
def pos_patterns(text):
    doc = nlp(text)
    patterns = []
    for i in range(len(doc)-1):
        token1, token2 = doc[i], doc[i+1]
        # Adjective + Noun (e.g. Machine Learning, problem-solving)
        if token1.pos_ == "ADJ" and token2.pos_ == "NOUN":
            patterns.append(token1.text + " " + token2.text)
        # Noun + Noun (e.g. Data Science)
        elif token1.pos_ == "NOUN" and token2.pos_ == "NOUN":
            patterns.append(token1.text + " " + token2.text)
    return patterns


# Method 3: Named Entity Recognition
def ner_skills(text):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT", "WORK_OF_ART"]:  # Product/Tech entities
            entities.append(ent.text)
    return entities


# Combine everything
def extract_all_skills(resume_text):
    keyword_skills = keyword_match(resume_text, SKILL_DATABASE)
    pattern_skills = pos_patterns(resume_text)
    ner_entities = ner_skills(resume_text)

    # Separate soft skills vs technical
    soft_found = []
    technical_found = []

    for skill in keyword_skills + pattern_skills + ner_entities:
        if skill.lower() in [s.lower() for s in SKILL_DATABASE['soft_skills']]:
            soft_found.append(skill)
        else:
            technical_found.append(skill)
            
    # Remove duplicates by converting to set, then back to list
    soft_found = list(set(soft_found))
    technical_found = list(set(technical_found))
    all_skills = list(set(soft_found + technical_found))

    return {
        'technical_skills': technical_found,
        'soft_skills': soft_found,
        'all_skills': all_skills
    }

# Test Input
resume = """
SKILLS:
Programming: Python, Java, JavaScript
Frameworks: TensorFlow, React, Django
Experience in Machine Learning and Deep Learning
Strong analytical and problem-solving skills
"""

print(extract_all_skills(resume))
