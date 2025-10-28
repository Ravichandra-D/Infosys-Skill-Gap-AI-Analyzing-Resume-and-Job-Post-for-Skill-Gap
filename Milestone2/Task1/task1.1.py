import re

def clean_resume_text(text):
    # Remove emails
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove phone numbers (patterns like +1-555-0123, (555) 123-4567, etc.)
    text = re.sub(r'\+?\d[\d\-\(\)\s]{7,}\d', '', text)
    
    # Remove URLs (http, https, www)
    text = re.sub(r'http\S+|www\.\S+', '', text)
    
    # Remove special characters except (+ # - .)
    text = re.sub(r'[^a-zA-Z0-9\s\+\#\-\.\,]', '', text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


# Test Input
text = """
Contact: john@email.com | Phone: +1-555-0123
Visit: www.johndoe.com
Skills: Python, C++, C#, .NET
"""

print(clean_resume_text(text))
