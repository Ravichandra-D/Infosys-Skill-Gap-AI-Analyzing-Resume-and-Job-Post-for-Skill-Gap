import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PERSON", "GPE", "PRODUCT"]:
            entities.append((ent.text, ent.label_))
    return entities


# Test Input
text = "John worked at Google and Microsoft in New York. He used TensorFlow and Python."
print(extract_entities(text))
