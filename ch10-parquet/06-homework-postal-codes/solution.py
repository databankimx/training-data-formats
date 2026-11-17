import os

import pyarrow.parquet as pq

path = os.path.join(os.environ["TRAINING_DATA"], "customers.parquet")
rows = pq.read_table(path).to_pylist()
# The postal code is a string, so its leading zeros are kept, and the first character is tested.
zero_start = sum(1 for row in rows if row["address"]["postal_code"].startswith("0"))
print(f"Postal codes starting with 0: {zero_start}")
