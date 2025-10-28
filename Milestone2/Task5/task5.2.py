def generate_skill_report(skills_dict):
    technical_skills = skills_dict.get("technical_skills", [])
    soft_skills = skills_dict.get("soft_skills", [])
    all_skills = skills_dict.get("all_skills", [])

    # Counts
    total_skills = len(all_skills)
    tech_count = len(technical_skills)
    soft_count = len(soft_skills)

    # Percentages (avoid division by zero)
    tech_percent = (tech_count / total_skills * 100) if total_skills > 0 else 0
    soft_percent = (soft_count / total_skills * 100) if total_skills > 0 else 0

    # Report formatting
    print("=== SKILL EXTRACTION REPORT ===\n")

    print(f"TECHNICAL SKILLS ({tech_count}):")
    for skill in sorted(technical_skills):
        print(f"  • {skill}")
    print()

    print(f"SOFT SKILLS ({soft_count}):")
    for skill in sorted(soft_skills):
        print(f"  • {skill}")
    print()

    print("SUMMARY:")
    print(f"  Total Skills: {total_skills}")
    print(f"  Technical: {tech_count} ({tech_percent:.0f}%)")
    print(f"  Soft Skills: {soft_count} ({soft_percent:.0f}%)")
# Example input from Question 5.1
skills_dict = {
    'technical_skills': ['Python', 'Java', 'JavaScript', 'TensorFlow',
                         'React', 'Django', 'Machine Learning', 'Deep Learning'],
    'soft_skills': ['analytical', 'problem-solving'],
    'all_skills': ['Python', 'Java', 'JavaScript', 'TensorFlow',
                   'React', 'Django', 'Machine Learning',
                   'Deep Learning', 'analytical', 'problem-solving']
}

generate_skill_report(skills_dict)
