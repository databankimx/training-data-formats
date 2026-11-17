import os
from decimal import Decimal

from openpyxl import load_workbook

path = os.path.join(os.environ["TRAINING_DATA"], "customers-text-numbers.xlsx")
workbook = load_workbook(path, data_only=True)
balances = [row[4] for row in workbook["customers"].iter_rows(min_row=2, values_only=True)]
text_count = sum(1 for value in balances if isinstance(value, str))
# Each text balance is converted through Decimal, so its digits are kept exactly.
total = sum((Decimal(value) for value in balances), Decimal("0"))
print(f"Text balances: {text_count}")
print(f"Text total: {total:.2f}")
