import os
from decimal import Decimal

import pyarrow.parquet as pq

path = os.path.join(os.environ["TRAINING_DATA"], "customers.parquet")
rows = pq.read_table(path).to_pylist()
vip = sum(1 for row in rows if "vip" in row["tags"])
# The balances are decimals in the file, so they are added as Decimal values, with no float conversion.
total = sum((row["balance"] for row in rows), Decimal("0"))
print(f"VIP customers: {vip}")
print(f"Total balance: {total:.2f}")
