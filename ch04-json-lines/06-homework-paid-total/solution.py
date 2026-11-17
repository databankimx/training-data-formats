import json
import os
from decimal import Decimal

path = os.path.join(os.environ["TRAINING_DATA"], "orders-lines.jsonl")
paid_count = 0
total = Decimal("0")
with open(path, encoding="utf-8") as handle:
    for line in handle:
        try:
            order = json.loads(line)
        except json.JSONDecodeError:
            continue
        if order["status"] == "paid":
            paid_count += 1
            # Decimal keeps each amount exact, so the sum has no floating-point drift.
            total += Decimal(order["amount"])
print(f"Paid orders: {paid_count}")
print(f"Paid total: {total:.2f}")
