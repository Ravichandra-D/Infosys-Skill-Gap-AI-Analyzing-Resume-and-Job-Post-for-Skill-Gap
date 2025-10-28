import spacy

# Load English model 
nlp = spacy.load("en_core_web_sm")

def tokenize_text(text):
    doc = nlp(text)
    tokens = []
    for token in doc:
        # Special handling for contractions
        if token.text.lower() in ["'m", "'re", "'s", "'ll", "'d", "'ve"]:
            if token.text.lower() == "'m":
                tokens.append("am")
            elif token.text.lower() == "'re":
                tokens.append("are")
            elif token.text.lower() == "'s":
                tokens.append("is")
            elif token.text.lower() == "'ll":
                tokens.append("will")
            elif token.text.lower() == "'d":
                tokens.append("would")
            elif token.text.lower() == "'ve":
                tokens.append("have")
        else:
            tokens.append(token.text)
    return tokens


# Test Input
text = "I'm a Python developer. I've worked on ML projects."
print(tokenize_text(text))
