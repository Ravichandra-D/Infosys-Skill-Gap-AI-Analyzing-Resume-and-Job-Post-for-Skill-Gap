import re
from collections import Counter

# Example skills (could be from SKILL_DATABASE)
SKILLS = ["Python", "Java", "JavaScript", "Machine Learning", "Deep Learning"]

def count_skill_frequency(text):
    text_lower = text.lower()
    counts = Counter()

    for skill in SKILLS:
        # regex whole-word or phrase match, case-insensitive
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        matches = re.findall(pattern, text_lower)
        if matches:
            counts[skill] = len(matches)

    # Sort by frequency (highest first)
    sorted_counts = dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))
    return sorted_counts


# ✅ Test Input
text = """
Python developer with Python experience. 
Used Python and Machine Learning. 
Machine Learning projects with Python.
"""

result = count_skill_frequency(text)

# Print nicely
for skill, freq in result.items():
    print(f"{skill}: {freq} times")
