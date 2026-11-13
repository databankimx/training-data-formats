import csv
import os

path = os.path.join(os.environ["TRAINING_DATA"], "customers-duplicates.csv")
with open(path, encoding="utf-8", newline="") as handle:
    body = list(csv.reader(handle))[1:]
seen = set()
failing = 0
for index, row in enumerate(body):
    customer_id = row[0]
    # A row fails when its identifier has already appeared on an earlier row.
    if customer_id in seen:
        print(f"Line {index + 2}: customer_id {customer_id} is a duplicate")
        failing += 1
    seen.add(customer_id)
print(f"Rows checked: {len(body)}")
print(f"Rows failing: {failing}")
