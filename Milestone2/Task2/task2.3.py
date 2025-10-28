import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

def find_adj_noun_patterns(text):
    doc = nlp(text)
    patterns = []

    for i in range(len(doc) - 1):
        # Look at current token and the next one
        token1, token2 = doc[i], doc[i+1]

        # If it's (ADJ + NOUN/PROPN) or (PROPN + NOUN/PROPN), treat as skill phrase
        if token1.pos_ in ["ADJ", "PROPN"] and token2.pos_ in ["NOUN", "PROPN"]:
            patterns.append(token1.text + " " + token2.text)

    return patterns


# Test Input
text = "Expert in Machine Learning, Deep Learning, and Natural Language Processing"
print(find_adj_noun_patterns(text))
