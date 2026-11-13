import os

names = ["customers.parquet", "customers.xlsx", "customers-as-json.csv"]


def kind_of(data: bytes) -> str:
    # Checks the signatures in order, and returns the first kind that matches.
    if data.startswith(b"PAR1"):
        return "parquet"
    if data.startswith(b"PK\x03\x04"):
        return "zip"
    if data.startswith(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"):
        return "ole2"
    if data.lstrip(b" \t\r\n")[:1] in (b"[", b"{"):
        return "json"
    if data.startswith(b"<?xml"):
        return "xml"
    if b"\x00" in data:
        return "binary"
    return "text"


for name in names:
    with open(os.path.join(os.environ["TRAINING_DATA"], name), "rb") as handle:
        print(f"{name}: {kind_of(handle.read())}")
