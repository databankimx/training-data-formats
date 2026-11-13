import os

path = os.path.join(os.environ["TRAINING_DATA"], "customers-mixed-line-endings.csv")
# Every LF is one line. A CRLF is an LF with a carriage return before it.
with open(path, "rb") as handle:
    data = handle.read()
lines = data.count(b"\n")
crlf = data.count(b"\r\n")
print(f"Lines: {lines}")
print(f"CRLF: {crlf}")
print(f"LF only: {lines - crlf}")
