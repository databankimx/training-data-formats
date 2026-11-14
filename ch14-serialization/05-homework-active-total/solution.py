import json
import os
from dataclasses import dataclass
from decimal import Decimal

path = os.path.join(os.environ["TRAINING_DATA"], "customers.json")


@dataclass
class Customer:
    customer_id: int
    active: bool
    balance: Decimal


with open(path, encoding="utf-8") as handle:
    customers = [Customer(record["customer_id"], record["active"], record["balance"]) for record in json.load(handle, parse_float=Decimal)]
active = [customer for customer in customers if customer.active]
total = sum((customer.balance for customer in active), Decimal("0"))
print(f"Active customers: {len(active)}")
print(f"Active total: {total:.2f}")
