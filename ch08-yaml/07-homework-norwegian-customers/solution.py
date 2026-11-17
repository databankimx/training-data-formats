import os

import yaml

path = os.path.join(os.environ["TRAINING_DATA"], "customers.yaml")
with open(path, encoding="utf-8") as handle:
    customers = yaml.safe_load(handle)
# The code is quoted in the file, so it arrives as text and compares as text.
norwegian = sum(1 for customer in customers if customer["country_code"] == "NO")
print(f"Norwegian customers: {norwegian}")
