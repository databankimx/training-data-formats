import os
from decimal import Decimal

import yaml

path = os.path.join(os.environ["TRAINING_DATA"], "customers.yaml")
with open(path, encoding="utf-8") as handle:
    customers = yaml.safe_load(handle)
vip = sum(1 for customer in customers if "vip" in customer["tags"])
# Decimal keeps each balance exact, so the total has no floating-point drift.
total = sum((Decimal(customer["balance"]) for customer in customers), Decimal("0"))
print(f"VIP customers: {vip}")
print(f"Total balance: {total:.2f}")
