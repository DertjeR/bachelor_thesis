from collections import Counter


simple_four = ["subjects", "verbs", "article", "nouns"]
simple_five = ["subjects", "verbs", "preposition", "article", "nouns"]
simple_six = ["subjects", "verbs", "preposition", "article", "adjectives", "nouns"]

simple_text_structure = (
    (simple_four + simple_five + simple_six) * 9) + simple_five

print(simple_text_structure)
print(Counter(simple_text_structure))
print(len(simple_text_structure))

complex1 = []
complex2 = []
complex3 = []

from collections import deque

octal_values = [1, 2, 3, 4]

while len(octal_values) != 0:
    octal_values = deque(octal_values)
    removed_value = octal_values.popleft()
    print(octal_values)

print(octal_values)