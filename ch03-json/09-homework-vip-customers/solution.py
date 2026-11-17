import json
import os

path = os.path.join(os.environ["TRAINING_DATA"], "customers.json")
with open(path, encoding="utf-8") as handle:
    customers = json.load(handle)
for customer in customers:
    # "in" checks the list itself, so a customer with no vip tag is skipped.
    if "vip" in customer["tags"]:
        print(f"{customer['customer_id']} {customer['address']['city']}")
