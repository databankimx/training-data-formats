import csv
import os

path = os.path.join(os.environ["TRAINING_DATA"], "customers-duplicates.csv")
with open(path, encoding="utf-8", newline="") as handle:
    records = list(csv.reader(handle))[1:]
seen = set()
repeated = []
for record in records:
    customer_id = record[0]
    if customer_id in seen and customer_id not in repeated:
        repeated.append(customer_id)
    seen.add(customer_id)
print(f"Rows: {len(records)}")
print(f"Unique customer ids: {len(seen)}")
print(f"Repeated ids: {', '.join(repeated)}")
