"""Builds every sample file for the data formats tutorial from dataset.py.

Run this once, on a machine with the generator's packages installed (see requirements-generator.txt). The
output is committed, so learners never need to run it. Running it again must produce the same bytes: the
workbook and Parquet timestamps are fixed, and every text file is written with LF line endings unless a
file is deliberately defective.

Customers.xls is the exception. It is committed as a fixed file and is not rebuilt by default, because the
xlwt writer stamps its document properties with timestamps that change on every run. Rebuild it only on
purpose, with --rebuild-xls, and then commit the result deliberately. verify() checks its contents instead.

Two kinds of file are produced:

* good files, which all describe the same customers and orders, so a conversion can be checked against
  the dataset;
* bad files, each of which teaches one failure. The name of each bad file says what is wrong with it.

Usage:
    python generate.py                build every file except customers.xls
    python generate.py --rebuild-xls  also rebuild customers.xls (see the warning above)
    python generate.py --verify       build every file except customers.xls, then check the good files
"""

from __future__ import annotations

import csv
import datetime as dt
import decimal
import io
import json
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

import openpyxl
import pyarrow as pa
import pyarrow.parquet as pq
import xlwt  # Legacy Excel writer (BSD license). Used only for the .xls sample, written in the old binary format.
import yaml

from dataset import CUSTOMERS, ORDERS

OUT = Path(__file__).resolve().parent
FIXED_TIMESTAMP = dt.datetime(2026, 1, 1, 0, 0, 0)

# ---------------------------------------------------------------------------
# Shapes shared by several formats
# ---------------------------------------------------------------------------


def flat_customer(c: dict) -> dict:
    """One customer as a flat row, for the formats that have no nesting (CSV, TSV, and Excel)."""
    return {
        "customer_id": c["customer_id"],
        "name": c["name"],
        "email": c["email"],
        "signup_date": c["signup_date"],
        "balance": c["balance"],
        "active": "true" if c["active"] else "false",
        "country_code": c["country_code"],
        "address_street": c["address"]["street"],
        "address_city": c["address"]["city"],
        "address_postal_code": c["address"]["postal_code"],
        "tags": ";".join(c["tags"]),
    }


CUSTOMER_COLUMNS = list(flat_customer(CUSTOMERS[0]).keys())
ORDER_COLUMNS = ["order_id", "customer_id", "order_date", "amount", "status"]


def flat_customers() -> list[dict]:
    return [flat_customer(c) for c in CUSTOMERS]


def json_customers() -> list[dict]:
    """The nested customers, with balance as a JSON number. JSON has no decimal type, so the value is a float here.

    The two decimal places are lost in the JSON number (0.00 becomes 0.0). The JSON lessons show that loss.
    """
    return [dict(c, balance=float(c["balance"])) for c in CUSTOMERS]


def to_csv(rows: list[dict], columns: list[str], delimiter: str = ",") -> str:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=columns, delimiter=delimiter, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def write_text(name: str, text: str) -> None:
    with open(OUT / name, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def write_bytes(name: str, data: bytes) -> None:
    (OUT / name).write_bytes(data)


# ---------------------------------------------------------------------------
# Good text files
# ---------------------------------------------------------------------------


def build_csv_family() -> None:
    write_text("customers.csv", to_csv(flat_customers(), CUSTOMER_COLUMNS))
    write_text("customers.tsv", to_csv(flat_customers(), CUSTOMER_COLUMNS, delimiter="\t"))
    write_text("orders.csv", to_csv(ORDERS, ORDER_COLUMNS))


def build_json_family() -> None:
    write_text("customers.json", json.dumps(json_customers(), indent=2, ensure_ascii=False) + "\n")
    lines = [json.dumps(c, ensure_ascii=False) for c in json_customers()]
    write_text("customers.jsonl", "\n".join(lines) + "\n")


def build_xml() -> None:
    root = ET.Element("customers")
    for c in CUSTOMERS:
        node = ET.SubElement(root, "customer", id=str(c["customer_id"]))
        ET.SubElement(node, "name").text = c["name"]
        ET.SubElement(node, "email").text = c["email"]
        ET.SubElement(node, "signup_date").text = c["signup_date"]
        ET.SubElement(node, "balance").text = c["balance"]
        ET.SubElement(node, "active").text = "true" if c["active"] else "false"
        ET.SubElement(node, "country_code").text = c["country_code"]
        address = ET.SubElement(node, "address")
        ET.SubElement(address, "street").text = c["address"]["street"]
        ET.SubElement(address, "city").text = c["address"]["city"]
        ET.SubElement(address, "postal_code").text = c["address"]["postal_code"]
        tags = ET.SubElement(node, "tags")
        for tag in c["tags"]:
            ET.SubElement(tags, "tag").text = tag
    ET.indent(root, space="  ")
    write_text("customers.xml", '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding="unicode") + "\n")

    root = ET.Element("orders")
    for o in ORDERS:
        node = ET.SubElement(root, "order", id=str(o["order_id"]))
        ET.SubElement(node, "customer_id").text = str(o["customer_id"])
        ET.SubElement(node, "order_date").text = o["order_date"]
        ET.SubElement(node, "amount").text = o["amount"]
        ET.SubElement(node, "status").text = o["status"]
    ET.indent(root, space="  ")
    write_text("orders.xml", '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding="unicode") + "\n")


def build_yaml() -> None:
    # PyYAML quotes the balance strings and the country code NO, so the good file reads back as text.
    text = yaml.safe_dump(CUSTOMERS, allow_unicode=True, sort_keys=False, default_flow_style=False)
    write_text("customers.yaml", text)


LAYOUT = [
    # column, first position (1-based), width, alignment
    ("customer_id", 1, 6, "right"),
    ("name", 8, 20, "left"),
    ("signup_date", 29, 10, "left"),
    ("balance", 40, 8, "right"),
    ("active", 49, 5, "left"),
    ("country_code", 55, 2, "left"),
]
FIXED_WIDTH = 60


def fixed_line(row: dict) -> str:
    buffer = [" "] * FIXED_WIDTH
    for column, start, width, align in LAYOUT:
        text = str(row[column])[:width]
        text = text.rjust(width) if align == "right" else text.ljust(width)
        buffer[start - 1 : start - 1 + width] = list(text)
    return "".join(buffer).rstrip()


def fixed_rows() -> list[dict]:
    return [
        {
            "customer_id": c["customer_id"],
            "name": c["name"],
            "signup_date": c["signup_date"],
            "balance": c["balance"],
            "active": "true" if c["active"] else "false",
            "country_code": c["country_code"],
        }
        for c in CUSTOMERS
    ]


def build_fixed() -> None:
    lines = [fixed_line(row) for row in fixed_rows()]
    write_text("customers.fixed", "\n".join(lines) + "\n")
    layout = [
        "Fixed-width layout for customers.fixed",
        "",
        "Positions are 1-based and inclusive. Each row is one customer, with no header row.",
        "",
        "column        start  width  alignment  notes",
    ]
    for column, start, width, align in LAYOUT:
        layout.append(f"{column:<13} {start:>5}  {width:>5}  {align:<9}")
    layout += [
        "",
        "Text columns are padded on the right with spaces. Numbers are padded on the left.",
        "A row is valid only if every column falls inside its positions.",
    ]
    write_text("customers.fixed.layout.txt", "\n".join(layout) + "\n")


# ---------------------------------------------------------------------------
# Excel and Parquet
# ---------------------------------------------------------------------------


def workbook_bytes(sheets: dict[str, tuple[list[str], list[list]]], text_cells: set[tuple[str, int, int]] = frozenset()) -> bytes:
    """Writes sheets of typed values. text_cells lists (sheet, row, column) cells to store as text on purpose."""
    book = openpyxl.Workbook()
    book.properties.creator = "DataBank training"
    book.properties.created = FIXED_TIMESTAMP
    book.properties.modified = FIXED_TIMESTAMP
    first = True
    for name, (headers, rows) in sheets.items():
        sheet = book.active if first else book.create_sheet()
        first = False
        sheet.title = name
        sheet.append(headers)
        for row_number, row in enumerate(rows, start=2):
            values = []
            for column_number, value in enumerate(row, start=1):
                if (name, row_number, column_number) in text_cells:
                    value = str(value)
                values.append(value)
            sheet.append(values)
    buffer = io.BytesIO()
    book.save(buffer)
    return buffer.getvalue()


def excel_rows() -> tuple[list[str], list[list]]:
    rows = []
    for c in CUSTOMERS:
        rows.append([
            c["customer_id"],
            c["name"],
            c["email"],
            dt.date.fromisoformat(c["signup_date"]),
            float(c["balance"]),
            c["active"],
            c["country_code"],
            c["address"]["street"],
            c["address"]["city"],
            c["address"]["postal_code"],
            ";".join(c["tags"]),
        ])
    return CUSTOMER_COLUMNS, rows


def orders_excel_rows() -> tuple[list[str], list[list]]:
    rows = [
        [o["order_id"], o["customer_id"], dt.date.fromisoformat(o["order_date"]), float(o["amount"]), o["status"]]
        for o in ORDERS
    ]
    return ORDER_COLUMNS, rows


def build_excel() -> None:
    customers_headers, customers_rows = excel_rows()
    orders_headers, orders_rows = orders_excel_rows()
    good = {"customers": (customers_headers, customers_rows), "orders": (orders_headers, orders_rows)}
    write_bytes("customers.xlsx", workbook_bytes(good))

    # Numbers stored as text: the cells look like numbers, but a formula or a sum treats them as text.
    text_numbers = {"customers": (customers_headers, customers_rows)}
    text_cells = set()
    for row_number in range(2, len(customers_rows) + 2):
        text_cells.add(("customers", row_number, 1))
        text_cells.add(("customers", row_number, 5))
    write_bytes("customers-text-numbers.xlsx", workbook_bytes(text_numbers, text_cells))

    # A cell that begins with "=" is stored as a formula. It runs when the workbook opens.
    formula_rows = [list(row) for row in customers_rows]
    formula_rows[0][1] = '=HYPERLINK("https://example.invalid","Alice Carter")'
    write_bytes("customers-formula.xlsx", workbook_bytes({"customers": (customers_headers, formula_rows)}))


# A legacy .xls workbook, in the binary format Excel used before 2007. It has the same two sheets as customers.xlsx.
# WARNING: customers.xls is committed. xlwt stamps its document properties with a timestamp on every run, so
# rebuilding changes the file's bytes. Run this only with --rebuild-xls, and commit the result on purpose.
# Its first bytes are the OLE2 signature, which the detector reports as ole2.
def build_xls() -> None:
    date_style = xlwt.easyxf(num_format_str="yyyy-mm-dd")
    book = xlwt.Workbook(encoding="utf-8")
    for name, (headers, rows) in (
        ("customers", excel_rows()),
        ("orders", orders_excel_rows()),
    ):
        sheet = book.add_sheet(name)
        for column, header in enumerate(headers):
            sheet.write(0, column, header)
        for row_number, row in enumerate(rows, start=1):
            for column, value in enumerate(row):
                if isinstance(value, dt.date):
                    sheet.write(row_number, column, value, date_style)
                else:
                    sheet.write(row_number, column, value)
    buffer = io.BytesIO()
    book.save(buffer)
    write_bytes("customers.xls", buffer.getvalue())


PARQUET_SCHEMA = pa.schema([
    ("customer_id", pa.int64()),
    ("name", pa.string()),
    ("email", pa.string()),
    ("signup_date", pa.date32()),
    ("balance", pa.decimal128(10, 2)),
    ("active", pa.bool_()),
    ("country_code", pa.string()),
    ("address", pa.struct([("street", pa.string()), ("city", pa.string()), ("postal_code", pa.string())])),
    ("tags", pa.list_(pa.string())),
])


def build_parquet() -> None:
    table = pa.Table.from_pydict(
        {
            "customer_id": [c["customer_id"] for c in CUSTOMERS],
            "name": [c["name"] for c in CUSTOMERS],
            "email": [c["email"] for c in CUSTOMERS],
            "signup_date": [dt.date.fromisoformat(c["signup_date"]) for c in CUSTOMERS],
            "balance": [decimal.Decimal(c["balance"]) for c in CUSTOMERS],
            "active": [c["active"] for c in CUSTOMERS],
            "country_code": [c["country_code"] for c in CUSTOMERS],
            "address": [c["address"] for c in CUSTOMERS],
            "tags": [c["tags"] for c in CUSTOMERS],
        },
        schema=PARQUET_SCHEMA,
    )
    sink = pa.BufferOutputStream()
    pq.write_table(table, sink, compression="none")
    write_bytes("customers.parquet", sink.getvalue().to_pybytes())


# ---------------------------------------------------------------------------
# Bad files: each one teaches one failure
# ---------------------------------------------------------------------------


def build_bad_text() -> None:
    rows = flat_customers()
    csv_text = to_csv(rows, CUSTOMER_COLUMNS)

    # A byte-order mark at the start of a UTF-8 file. Some readers show it as a stray character in the first header.
    write_bytes("customers-utf8-bom.csv", ("\ufeff" + csv_text).encode("utf-8"))

    # Windows-1252 text. Characters that Windows-1252 cannot hold, such as the Polish Ł, are replaced with "?".
    write_bytes("customers-windows-1252.csv", csv_text.encode("cp1252", errors="replace"))

    # Alternate rows end in CRLF and the others in LF.
    lines = csv_text.splitlines()
    mixed = "".join(line + ("\r\n" if index % 2 else "\n") for index, line in enumerate(lines))
    write_text("customers-mixed-line-endings.csv", mixed)

    # JSON content under a .csv name. The first three records, as JSON.
    write_text("customers-as-json.csv", json.dumps(json_customers()[:3], indent=2, ensure_ascii=False) + "\n")

    # Ragged rows: row 3 loses its last field, and row 6 gains one.
    ragged = csv_text.splitlines()
    ragged[3] = ragged[3].rsplit(",", 1)[0]
    ragged[6] = ragged[6] + ",extra"
    write_text("customers-ragged.csv", "\n".join(ragged) + "\n")

    # A cell that begins with "=", which a spreadsheet would run.
    formula_rows = flat_customers()
    formula_rows[0]["name"] = '=HYPERLINK("https://example.invalid","Alice Carter")'
    write_text("customers-formula.csv", to_csv(formula_rows, CUSTOMER_COLUMNS))

    # A quoted field that contains a line break.
    newline_rows = flat_customers()
    newline_rows[0]["address_street"] = "12 Maple\nStreet"
    write_text("customers-embedded-newline.csv", to_csv(newline_rows, CUSTOMER_COLUMNS))

    # Dates in three different forms, and one that does not exist (February 30).
    dated = flat_customers()[:6]
    dated[0]["signup_date"] = "14/03/2021"
    dated[1]["signup_date"] = "March 14, 2021"
    dated[2]["signup_date"] = "2021-02-30"
    write_text("customers-bad-dates.csv", to_csv(dated, CUSTOMER_COLUMNS))

    # Repeated customers, one with a changed balance and one exact repeat.
    duplicates = flat_customers()
    changed = dict(flat_customers()[2], balance="1100.00")
    duplicates.append(changed)
    duplicates.append(flat_customers()[6])
    write_text("customers-duplicates.csv", to_csv(duplicates, CUSTOMER_COLUMNS))

    # A JSON file cut off partway through.
    full = json.dumps(json_customers(), indent=2, ensure_ascii=False) + "\n"
    write_text("customers-truncated.json", full[: int(len(full) * 0.6)])

    # Integers too large for an IEEE 754 double, which some readers round silently.
    write_text(
        "customers-big-numbers.json",
        """[
  {
    "customer_id": 9007199254740993,
    "name": "Test Account One",
    "balance": 1250.75
  },
  {
    "customer_id": 12345678901234567890,
    "name": "Test Account Two",
    "balance": 0.5
  }
]
""",
    )

    # Nulls, empty strings, and missing keys, which mean different things in a real system.
    write_text(
        "customers-null-mix.json",
        """[
  {"customer_id": 1001, "name": "Alice Carter", "email": null, "tags": []},
  {"customer_id": 1002, "name": "", "email": "chidi.okafor@example.invalid", "tags": null},
  {"customer_id": 1003, "name": "Renée Dubois", "tags": ["newsletter"]}
]
""",
    )

    # One orders line is malformed. The rest of the file is valid.
    order_lines = [json.dumps(o) for o in ORDERS]
    order_lines[6] = order_lines[6][:-1]
    write_text("orders-lines.jsonl", "\n".join(order_lines) + "\n")

    # A fixed-width row shorter than the layout.
    fixed = [fixed_line(row) for row in fixed_rows()]
    fixed[2] = fixed[2][:30]
    write_text("customers-fixed-short-row.fixed", "\n".join(fixed) + "\n")

    # An external entity that points at a file. The path is a reserved example that does not exist anywhere.
    write_text(
        "orders-xxe.xml",
        """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE order [
  <!ENTITY secret SYSTEM "file:///example/secret-notes.txt">
]>
<orders>
  <order id="5001">
    <customer_id>1001</customer_id>
    <order_date>2025-01-08</order_date>
    <amount>129.99</amount>
    <status>shipped</status>
    <note>&secret;</note>
  </order>
</orders>
""",
    )

    # Plain scalars that YAML 1.1 reads as booleans: NO (Norway) and on.
    write_text(
        "config-norway.yaml",
        """countries:
  - code: NO
    name: Norway
  - code: DE
    name: Germany
settings:
  notifications: on
  retry: 3
""",
    )

    # A tab used for indentation, which YAML does not allow.
    write_text(
        "config-yaml-tabs.yaml",
        "settings:\n\tretry: 3\n\ttimeout: 30\n",
    )


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------


def verify() -> None:
    """Reads the good files back and checks them against the dataset. Raises AssertionError on a mismatch."""
    expected_ids = [c["customer_id"] for c in CUSTOMERS]

    rows = list(csv.DictReader(open(OUT / "customers.csv", encoding="utf-8", newline="")))
    assert [int(r["customer_id"]) for r in rows] == expected_ids, "customers.csv ids"
    assert rows[1]["name"] == "Okafor, Chidi", "customers.csv quoted comma"

    tsv = list(csv.DictReader(open(OUT / "customers.tsv", encoding="utf-8", newline=""), delimiter="\t"))
    assert len(tsv) == len(CUSTOMERS), "customers.tsv row count"

    data = json.loads((OUT / "customers.json").read_text(encoding="utf-8"))
    assert [c["customer_id"] for c in data] == expected_ids, "customers.json ids"
    assert data[0]["address"]["city"] == "Springfield", "customers.json nested address"

    lines = (OUT / "customers.jsonl").read_text(encoding="utf-8").splitlines()
    assert [json.loads(line)["customer_id"] for line in lines] == expected_ids, "customers.jsonl ids"

    yaml_data = yaml.safe_load((OUT / "customers.yaml").read_text(encoding="utf-8"))
    assert yaml_data[3]["country_code"] == "NO", "customers.yaml keeps NO as text"
    assert yaml_data[0]["balance"] == "1250.75", "customers.yaml keeps balance as text"

    root = ET.parse(OUT / "customers.xml").getroot()
    assert [int(node.get("id")) for node in root] == expected_ids, "customers.xml ids"

    book = openpyxl.load_workbook(OUT / "customers.xlsx", data_only=True)
    sheet = book["customers"]
    assert sheet.cell(row=2, column=1).value == expected_ids[0], "customers.xlsx first id"

    import xlrd  # Legacy Excel reader (BSD license). Opens customers.xls and checks its contents.

    xls = xlrd.open_workbook(OUT / "customers.xls")
    customers_sheet = xls.sheet_by_name("customers")
    assert customers_sheet.nrows == len(CUSTOMERS) + 1, "customers.xls has one row per customer"
    assert int(customers_sheet.cell_value(1, 0)) == expected_ids[0], "customers.xls first id"
    assert customers_sheet.cell_value(1, 1) == CUSTOMERS[0]["name"], "customers.xls first name"
    orders_sheet = xls.sheet_by_name("orders")
    assert orders_sheet.nrows == len(ORDERS) + 1, "customers.xls has one row per order"
    assert int(orders_sheet.cell_value(1, 0)) == ORDERS[0]["order_id"], "customers.xls first order id"

    table = pq.read_table(OUT / "customers.parquet")
    assert table.column("customer_id").to_pylist() == expected_ids, "customers.parquet ids"
    assert str(table.column("balance")[0]) == "1250.75", "customers.parquet decimal"

    print("verify: every good file reads back to the dataset")


def main() -> None:
    build_csv_family()
    build_json_family()
    build_xml()
    build_yaml()
    build_fixed()
    build_excel()
    if "--rebuild-xls" in sys.argv:
        build_xls()
    build_parquet()
    build_bad_text()
    print(f"wrote sample files to {OUT}")
    if "--verify" in sys.argv:
        verify()


if __name__ == "__main__":
    main()
