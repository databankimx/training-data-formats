import re

# Inline data, not from a sample file. Name, country code, and email for three customers.
records = [
    ("  Alice   Carter ", "us", "alice@example.invalid"),
    ("Chidi Okafor", "GB", ""),
    ("Mei\u00a0Lin", "SG", "mei@example.invalid"),
]
changed = 0
review = 0
for name, country, email in records:
    cleaned_name = re.sub(r"\s+", " ", name).strip()
    if cleaned_name != name:
        changed += 1
    cleaned_country = country.strip().upper()
    if cleaned_country != country:
        changed += 1
    if email == "":
        review += 1
print(f"Changed values: {changed}")
print(f"Values needing review: {review}")
