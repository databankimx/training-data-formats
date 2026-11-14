import csv
import os
from decimal import Decimal

path = os.path.join(os.environ["TRAINING_DATA"], "orders.csv")
with open(path, encoding="utf-8", newline="") as handle:
    orders = list(csv.DictReader(handle))
shipped = [order for order in orders if order["status"] == "shipped"]
customers = {order["customer_id"] for order in shipped}
total = sum((Decimal(order["amount"]) for order in shipped), Decimal("0"))
print(f"Customers with a shipped order: {len(customers)}")
print(f"Shipped total: {total:.2f}")
