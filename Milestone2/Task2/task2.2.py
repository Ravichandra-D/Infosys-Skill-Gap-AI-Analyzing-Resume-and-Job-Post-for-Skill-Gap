import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

def extract_nouns(text):
    doc = nlp(text)
    # Keep only NOUN and PROPN tokens
    nouns = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]
    return nouns


# Test Input
text = "Experienced Data Scientist proficient in Machine Learning and Python programming"
print(extract_nouns(text))
