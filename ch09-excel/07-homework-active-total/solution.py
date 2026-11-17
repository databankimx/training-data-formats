import os
from decimal import Decimal

from openpyxl import load_workbook

path = os.path.join(os.environ["TRAINING_DATA"], "customers.xlsx")
workbook = load_workbook(path, data_only=True)
rows = list(workbook["customers"].iter_rows(min_row=2, values_only=True))
# Column 6 is active, and column 5 is balance. A stored number is converted through its text, so the cents survive.
active = sum(1 for row in rows if row[5] is True)
total = sum((Decimal(str(row[4])).quantize(Decimal("0.01")) for row in rows), Decimal("0"))
print(f"Active customers: {active}")
print(f"Total balance: {total:.2f}")
