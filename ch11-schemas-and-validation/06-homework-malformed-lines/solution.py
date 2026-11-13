import json
import os

# Inline data, not from a sample file. The statuses an order may have.
allowed = {"pending", "paid", "shipped", "refunded"}
path = os.path.join(os.environ["TRAINING_DATA"], "orders-lines.jsonl")
checked = 0
failing = 0
with open(path, encoding="utf-8") as handle:
    for number, line in enumerate(handle, start=1):
        checked += 1
        try:
            order = json.loads(line)
        except json.JSONDecodeError:
            print(f"Line {number}: not valid JSON")
            failing += 1
            continue
        if order.get("status") not in allowed:
            print(f"Line {number}: status is not allowed")
            failing += 1
print(f"Lines checked: {checked}")
print(f"Lines failing: {failing}")
