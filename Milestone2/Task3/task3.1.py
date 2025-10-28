# Skill Database with Programming Languages, Frameworks, Databases, Cloud, and Soft Skills

SKILL_DATABASE = {
    'programming_languages': [
        'Python', 'Java', 'C', 'C++', 'C#',
        'JavaScript', 'R', 'Go', 'Ruby', 'PHP'
    ],
    'frameworks': [
        'TensorFlow', 'PyTorch', 'Scikit-learn', 'Keras', 'React',
        'Angular', 'Django', 'Flask', 'Spring', 'Node.js'
    ],
    'databases': [
        'MySQL', 'PostgreSQL', 'MongoDB', 'SQLite', 'Oracle'
    ],
    'cloud': [
        'AWS', 'Azure', 'Google Cloud', 'IBM Cloud', 'Heroku'
    ],
    'soft_skills': [
        'Leadership', 'Teamwork', 'Communication', 'Problem-solving', 'Time Management'
    ]
}


# Test print
for category, skills in SKILL_DATABASE.items():
    print(f"{category.capitalize()}: {skills}")
