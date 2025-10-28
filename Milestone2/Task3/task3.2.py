import re
def extract_skills(text, skill_database):
    found_skills = {}

    # Convert text to lowercase for case-insensitive matching
    text_lower = text.lower()

    # Loop through categories and skills
    for category, skills in skill_database.items():
        matched = []
        for skill in skills:
            # Use regex to match whole words (case-insensitive)
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                matched.append(skill)
        
        if matched:  # Only add non-empty categories
            found_skills[category] = matched

    return found_skills

# Example SKILL_DATABASE
SKILL_DATABASE = {
    'programming_languages': ['Python', 'Java', 'C', 'C++', 'C#', 'JavaScript', 'R', 'Go', 'Ruby', 'PHP'],
    'frameworks': ['TensorFlow', 'PyTorch', 'Scikit-learn', 'Keras', 'React', 'Angular', 'Django', 'Flask', 'Spring', 'Node.js'],
    'databases': ['MySQL', 'PostgreSQL', 'MongoDB', 'SQLite', 'Oracle'],
    'cloud': ['AWS', 'Azure', 'Google Cloud', 'IBM Cloud', 'Heroku'],
    'soft_skills': ['Leadership', 'Teamwork', 'Communication', 'Problem-solving', 'Time Management']
}
# Test Input
text = "Proficient in Python, Java, TensorFlow, and AWS. Strong leadership skills."
print(extract_skills(text, SKILL_DATABASE))
