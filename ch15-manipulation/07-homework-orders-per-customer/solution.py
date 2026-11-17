import csv
import os
from collections import Counter

path = os.path.join(os.environ["TRAINING_DATA"], "orders.csv")
with open(path, encoding="utf-8", newline="") as handle:
    orders = list(csv.DictReader(handle))
sizes = Counter(order["customer_id"] for order in orders).values()
print(f"Customers with more than one order: {sum(1 for size in sizes if size > 1)}")
print(f"Most orders by one customer: {max(sizes)}")
