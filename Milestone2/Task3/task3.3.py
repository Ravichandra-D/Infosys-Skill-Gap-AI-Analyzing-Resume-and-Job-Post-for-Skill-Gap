# Abbreviation mapping dictionary
ABBREVIATIONS = {
    'ML': 'Machine Learning',
    'DL': 'Deep Learning',
    'NLP': 'Natural Language Processing',
    'AI': 'Artificial Intelligence',
    'DS': 'Data Science',
    'CV': 'Computer Vision',
    'JS': 'JavaScript',
    'TS': 'TypeScript',
    'K8s': 'Kubernetes',
    'GCP': 'Google Cloud Platform',
    'AWS': 'AWS',   # Keep same if abbreviation is widely used
    'SQL': 'Structured Query Language'
}

def normalize_skills(skill_list):
    normalized = []
    for skill in skill_list:
        # If abbreviation exists, replace with full form
        if skill in ABBREVIATIONS:
            normalized.append(ABBREVIATIONS[skill])
        else:
            normalized.append(skill)  # Keep as is if not abbreviation
    return normalized


# Test Input
skills = ['ML', 'DL', 'NLP', 'JS', 'K8s', 'AWS', 'GCP']
print(normalize_skills(skills))
