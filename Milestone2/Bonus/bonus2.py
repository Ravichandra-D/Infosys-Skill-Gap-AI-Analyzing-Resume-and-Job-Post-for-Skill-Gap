import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

def extract_skill_context(text, skill):
    doc = nlp(text)
    contexts = []
    skill_lower = skill.lower()

    for sent in doc.sents:  # Iterate through sentences
        if skill_lower in sent.text.lower():
            contexts.append(sent.text.strip())

    # Print output
    print(f"Skill: {skill}")
    for i, ctx in enumerate(contexts, start=1):
        print(f"Context {i}: \"{ctx}\"")
    
    return contexts


# ✅ Test Input
text = """
I am a Python developer. I have 5 years of experience in Python.
Also worked on Java projects. Python is my primary language.
"""
skill = "Python"

extract_skill_context(text, skill)
