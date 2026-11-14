import csv
import os

path = os.path.join(os.environ["TRAINING_DATA"], "customers.csv")
with open(path, encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle))
total = 0
empty = 0
for row in rows:
    # Empty items are dropped, so a customer with no tags has an empty list, not a list with one empty item.
    tags = [tag for tag in row["tags"].split(";") if tag]
    total += len(tags)
    if not tags:
        empty += 1
print(f"Tags in the list: {total}")
print(f"Customers with no tags: {empty}")
