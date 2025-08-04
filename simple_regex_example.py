#!/usr/bin/env python3
"""
Simple regex example to find "Dave is cool" in text.
"""

import re

# The phrase we're looking for
phrase = "Dave is cool"

# Create regex pattern
# re.escape() handles any special regex characters in the phrase
pattern = re.compile(re.escape(phrase))

# For case-insensitive search:
pattern_case_insensitive = re.compile(re.escape(phrase), re.IGNORECASE)

# Example text
sample_text = """
This is a sample document.
I heard that Dave is cool.
Some people say DAVE IS COOL too!
But dave is cool is not matched by default (lowercase).
Dave is cool appears multiple times here. Dave is cool!
"""

print("Basic Regex Pattern:")
print(f"Pattern: {pattern.pattern}")
print("\nSearching for exact matches (case-sensitive):")

# Find all matches
matches = list(pattern.finditer(sample_text))
print(f"Found {len(matches)} matches")

for match in matches:
    start = match.start()
    end = match.end()
    # Find line number
    line_num = sample_text[:start].count('\n') + 1
    print(f"  Match at position {start}-{end}, line {line_num}: '{match.group()}'")

print("\n" + "="*50 + "\n")

print("Case-insensitive search:")
matches_ci = list(pattern_case_insensitive.finditer(sample_text))
print(f"Found {len(matches_ci)} matches")

for match in matches_ci:
    start = match.start()
    end = match.end()
    line_num = sample_text[:start].count('\n') + 1
    print(f"  Match at position {start}-{end}, line {line_num}: '{match.group()}'")

# For searching in a large file
print("\n" + "="*50 + "\n")
print("For searching in large files (80M pages), use the search_dave.py script:")
print("  python search_dave.py your_document.txt")
print("  python search_dave.py your_document.txt -i  # case-insensitive")
print("  python search_dave.py your_document.txt -m  # use memory mapping for huge files")
print("  python search_dave.py your_document.txt -c  # count only")
print("  python search_dave.py your_document.txt -n 100  # show first 100 matches")