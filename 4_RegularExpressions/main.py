import random

from generator import Generator
from steps import steps
from patterns import RegexPatterns

def print_examples(title, pattern_name, examples):
    print(f"\n[{title}]")
    print("Regular Expression:", RegexPatterns.VARIANT_4[pattern_name])
    print("How it works:")
    for step in steps(pattern_name):
        print("  -", step)
    print("Examples:")
    random.shuffle(examples)
    for ex in examples[:10]:  # show only first 10
        print(" ", ex)

print("REGULAR EXPRESSION GENERATOR (VARIANT 4)\n")

generator = Generator()

regex_1_examples = generator.generate_regex_1()
print_examples("Regular Expression 1", "regex_1", regex_1_examples)

regex_2_examples = generator.generate_regex_2()
print_examples("Regular Expression 2", "regex_2", regex_2_examples)

regex_3_examples = generator.generate_regex_3()
print_examples("Regular Expression 3", "regex_3", regex_3_examples)

