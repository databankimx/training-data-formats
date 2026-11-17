import csv
import os

path = os.path.join(os.environ["TRAINING_DATA"], "customers.csv")
with open(path, encoding="utf-8", newline="") as handle:
    rows = list(csv.reader(handle))[1:]
# Column 5 is active, and column 10 is tags.
active = sum(1 for row in rows if row[5] == "true")
tagged = sum(1 for row in rows if row[10] != "")
print(f"Active customers: {active}")
print(f"Tagged customers: {tagged}")
