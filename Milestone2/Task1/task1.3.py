import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

def remove_stop_words(text):
    # Copy spaCy's stop words
    stop_words = nlp.Defaults.stop_words.copy()

    # Make sure programming languages are NOT treated as stopwords
    for lang in ["c", "r", "go", "d"]:
        if lang in stop_words:
            stop_words.remove(lang)

    # Tokenize text
    doc = nlp(text)

    # Keep words that are NOT stop words
    cleaned_tokens = [token.text for token in doc if token.text.lower() not in stop_words]

    # Join back into a string
    return " ".join(cleaned_tokens)


# Test Input
text = "I have experience in Python and R programming with excellent skills in C and Go"
print(remove_stop_words(text))
