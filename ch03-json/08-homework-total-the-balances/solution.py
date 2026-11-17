import json
import os
from decimal import Decimal

path = os.path.join(os.environ["TRAINING_DATA"], "customers.json")
# parse_float=Decimal keeps each balance exact, instead of storing it as a binary float.
with open(path, encoding="utf-8") as handle:
    customers = json.load(handle, parse_float=Decimal)
active = sum(1 for customer in customers if customer["active"])
total = sum((customer["balance"] for customer in customers), Decimal("0"))
print(f"Active customers: {active}")
print(f"Total balance: {total:.2f}")
