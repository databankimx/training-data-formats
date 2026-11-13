import json
import os

path = os.path.join(os.environ["TRAINING_DATA"], "orders-lines.jsonl")
shipped = 0
skipped = 0
with open(path, encoding="utf-8") as handle:
    for line in handle:
        try:
            order = json.loads(line)
        except json.JSONDecodeError:
            skipped += 1
            continue
        if order["status"] == "shipped":
            shipped += 1
print(f"Shipped orders: {shipped}")
print(f"Skipped lines: {skipped}")
