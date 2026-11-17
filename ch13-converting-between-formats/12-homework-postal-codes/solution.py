import csv
import os

path = os.path.join(os.environ["TRAINING_DATA"], "customers.csv")
with open(path, encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle))
changed = 0
for row in rows:
    code = row["address_postal_code"]
    # Only all-digit codes are numbers. Each is converted to a number and back, and compared as text.
    if not code.isdigit():
        continue
    if str(int(code)) != code:
        changed += 1
print(f"Postal codes that change: {changed}")
