import os
from decimal import Decimal

path = os.path.join(os.environ["TRAINING_DATA"], "customers-fixed-short-row.fixed")
layout_length = 56
with open(path, encoding="utf-8", newline="") as handle:
    lines = handle.read().splitlines()
counted = 0
skipped = 0
# Decimal keeps each balance exact, so the total has no floating-point drift.
total = Decimal("0")
for line in lines:
    if len(line) < layout_length:
        skipped += 1
        continue
    if line[48:53].strip() == "true":
        counted += 1
        total += Decimal(line[39:47].strip())
print(f"Active customers counted: {counted}")
print(f"Active total: {total:.2f}")
print(f"Skipped short lines: {skipped}")
