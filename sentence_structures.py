from collections import Counter


simple_four = ["subjects", "verbs", "article", "nouns"]
simple_five = ["subjects", "verbs", "preposition", "article", "nouns"]
simple_six = ["subjects", "verbs", "preposition", "article", "adjectives", "nouns"]

simple_text_structure = ((simple_four + simple_five + simple_six) * 9) + simple_five
print(simple_text_structure)
print(Counter(simple_text_structure))
print(len(simple_text_structure))

complex1 = []
complex2 = []
complex3 = []