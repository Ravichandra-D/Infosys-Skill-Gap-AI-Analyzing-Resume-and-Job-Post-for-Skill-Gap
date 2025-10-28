import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

def pos_tag_resume(text):
    doc = nlp(text)
    # Create (word, POS) tuples
    pos_tags = [(token.text, token.pos_) for token in doc]
    return pos_tags


# Test Input
text = "John is an experienced Python developer"
print(pos_tag_resume(text))
