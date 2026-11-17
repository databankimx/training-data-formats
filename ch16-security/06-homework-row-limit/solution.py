import os

path = os.path.join(os.environ["TRAINING_DATA"], "customers.csv")
limit = 10
accepted = 0
refused = 0
with open(path, encoding="utf-8") as handle:
    next(handle)  # The header is not a data row, so it is skipped.
    for _ in handle:
        if accepted < limit:
            accepted += 1
        else:
            refused += 1
print(f"Rows accepted: {accepted}")
print(f"Rows refused: {refused}")
