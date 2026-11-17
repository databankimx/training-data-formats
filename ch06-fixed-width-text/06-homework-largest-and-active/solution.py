import os
from decimal import Decimal

path = os.path.join(os.environ["TRAINING_DATA"], "customers.fixed")
with open(path, encoding="utf-8", newline="") as handle:
    lines = handle.read().splitlines()
active = 0
largest = None
largest_text = ""
for line in lines:
    # The active flag is at positions 49 to 53, and the balance at positions 40 to 47.
    if line[48:53].strip() == "true":
        active += 1
    text = line[39:47].strip()
    value = Decimal(text)
    if largest is None or value > largest:
        largest = value
        largest_text = text
print(f"Active customers: {active}")
print(f"Largest balance: {largest_text}")
