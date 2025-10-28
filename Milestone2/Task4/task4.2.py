TRAIN_DATA = [
    # Sentence 1
    ("Python developer with 5 years of experience", 
     {"entities": [(0, 6, "SKILL")]}),
    
    # Sentence 2
    ("Expert in Machine Learning and Data Science",
     {"entities": [(10, 26, "SKILL"), (31, 43, "SKILL")]}),
    
    # Sentence 3
    ("Proficient in TensorFlow and PyTorch frameworks",
     {"entities": [(13, 23, "SKILL"), (28, 35, "SKILL")]}),
    
    # Sentence 4
    ("Strong SQL and MongoDB database skills",
     {"entities": [(7, 10, "SKILL"), (15, 21, "SKILL")]}),
    
    # Sentence 5
    ("Excellent communication and leadership abilities",
     {"entities": [(10, 23, "SKILL"), (28, 38, "SKILL")]}),
]
# Print TRAIN_DATA to verify
for data in TRAIN_DATA:
    print(data)