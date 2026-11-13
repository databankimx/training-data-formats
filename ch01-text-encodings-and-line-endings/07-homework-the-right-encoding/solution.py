import os

path = os.path.join(os.environ["TRAINING_DATA"], "customers-windows-1252.csv")
# Decode with the encoding the file was written in. The letter is given as an escape, so the source is plain ASCII.
with open(path, encoding="cp1252", newline="") as handle:
    lines = handle.read().splitlines()
count = sum(1 for line in lines if "\u00e9" in line)
print(f"Lines containing e-acute: {count}")
