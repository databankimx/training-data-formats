import os

names = ["customers-utf8-bom.csv", "customers-windows-1252.csv", "config-norway.yaml"]

for name in names:
    with open(os.path.join(os.environ["TRAINING_DATA"], name), "rb") as handle:
        data = handle.read()
    # The mark is checked on the bytes, before anything is decoded.
    has_mark = data.startswith(b"\xef\xbb\xbf")
    # A file with no NUL byte is text. The mark doesn't change that.
    kind = "binary" if b"\x00" in data else "text"
    suffix = ", with byte-order mark" if has_mark else ""
    print(f"{name}: {kind}{suffix}")
