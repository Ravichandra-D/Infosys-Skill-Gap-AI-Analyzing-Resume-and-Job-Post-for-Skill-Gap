import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

def lemmatize_text(text):
    doc = nlp(text)
    # Use token.lemma_ to get base form
    lemmatized_tokens = [token.lemma_ for token in doc]
    # Join back to a string
    return " ".join(lemmatized_tokens)


# Test Input
text = "I am working on developing multiple applications using programming languages"
print(lemmatize_text(text))
