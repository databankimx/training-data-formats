import os

path = os.path.join(os.environ["TRAINING_DATA"], "customers-utf8-bom.csv")
# The mark is the three bytes EF BB BF. Check the bytes first, then decode without the mark.
with open(path, "rb") as handle:
    data = handle.read()
has_mark = data.startswith(b"\xef\xbb\xbf")
text = data[3:].decode("utf-8") if has_mark else data.decode("utf-8")
header = text.split("\n")[0].split(",")[0]
print(f"Starts with a byte-order mark: {'yes' if has_mark else 'no'}")
print(f"First header: {header}")
