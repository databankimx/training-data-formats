"""Tests for the sample files in this folder.

Run from this folder, with the generator's packages installed:

    python -m pytest

The tests read the committed files. They never change them. The regeneration test builds every file into a
temporary folder and checks that the bytes match the committed files, so a change to generate.py that alters
the output is caught here.
"""

import csv
import datetime as dt
import json
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

import openpyxl
import pyarrow.parquet as pq
import pytest
import xlrd
import yaml

import generate
from dataset import CUSTOMERS, ORDERS

DATA = Path(__file__).resolve().parent
CUSTOMER_IDS = [c["customer_id"] for c in CUSTOMERS]
ORDER_IDS = [o["order_id"] for o in ORDERS]


def read_text(name):
    return (DATA / name).read_text(encoding="utf-8")


def read_csv(name, delimiter=","):
    with open(DATA / name, encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=delimiter))


# ---------------------------------------------------------------------------
# Good files read back to the dataset
# ---------------------------------------------------------------------------


def test_csv_reads_back_with_quoted_comma():
    rows = read_csv("customers.csv")
    assert [int(r["customer_id"]) for r in rows] == CUSTOMER_IDS
    assert rows[1]["name"] == "Okafor, Chidi"


def test_tsv_reads_back():
    rows = read_csv("customers.tsv", delimiter="\t")
    assert [int(r["customer_id"]) for r in rows] == CUSTOMER_IDS


def test_orders_csv_reads_back():
    rows = read_csv("orders.csv")
    assert [int(r["order_id"]) for r in rows] == ORDER_IDS
    assert [r["amount"] for r in rows] == [o["amount"] for o in ORDERS]


def test_json_reads_back_with_nested_address():
    data = json.loads(read_text("customers.json"))
    assert [c["customer_id"] for c in data] == CUSTOMER_IDS
    assert data[0]["address"]["city"] == "Springfield"


def test_jsonl_has_one_object_per_customer():
    lines = read_text("customers.jsonl").splitlines()
    assert [json.loads(line)["customer_id"] for line in lines] == CUSTOMER_IDS


def test_yaml_keeps_norway_code_and_balance_as_text():
    data = yaml.safe_load(read_text("customers.yaml"))
    assert [c["customer_id"] for c in data] == CUSTOMER_IDS
    assert data[3]["country_code"] == "NO"
    assert data[0]["balance"] == "1250.75"


def test_xml_customers_and_orders_read_back():
    customers = ET.parse(DATA / "customers.xml").getroot()
    orders = ET.parse(DATA / "orders.xml").getroot()
    assert [int(node.get("id")) for node in customers] == CUSTOMER_IDS
    assert [int(node.get("id")) for node in orders] == ORDER_IDS


def test_fixed_width_rows_match_the_layout():
    lines = read_text("customers.fixed").splitlines()
    assert len(lines) == len(CUSTOMERS)
    for line, customer in zip(lines, CUSTOMERS):
        assert int(line[0:6]) == customer["customer_id"]
        assert line[7:27].rstrip() == customer["name"][:20]
        assert line[28:38] == customer["signup_date"]
        assert line[54:56] == customer["country_code"]
    assert (DATA / "customers.fixed.layout.txt").exists()


def test_xlsx_has_two_sheets_with_typed_dates():
    book = openpyxl.load_workbook(DATA / "customers.xlsx")
    assert book.sheetnames == ["customers", "orders"]
    customers = book["customers"]
    assert customers.max_row == len(CUSTOMERS) + 1
    assert customers.cell(row=2, column=4).value == dt.datetime(2021, 3, 14)
    assert book["orders"].max_row == len(ORDERS) + 1


def test_xls_has_the_same_two_sheets():
    book = xlrd.open_workbook(DATA / "customers.xls")
    assert book.sheet_names() == ["customers", "orders"]
    assert book.sheet_by_name("customers").nrows == len(CUSTOMERS) + 1
    assert book.sheet_by_name("orders").nrows == len(ORDERS) + 1


def test_parquet_reads_back_with_decimal_balance():
    table = pq.read_table(DATA / "customers.parquet")
    assert table.column("customer_id").to_pylist() == CUSTOMER_IDS
    assert str(table.column("balance")[0]) == "1250.75"


def test_generator_verify_passes_on_committed_files(monkeypatch):
    monkeypatch.setattr(generate, "OUT", DATA)
    generate.verify()


def workbook_cells(path):
    book = openpyxl.load_workbook(path)
    return {sheet.title: [[cell.value for cell in row] for row in sheet.iter_rows()] for sheet in book}


def test_regenerating_reproduces_the_committed_files(tmp_path, monkeypatch):
    monkeypatch.setattr(generate, "OUT", tmp_path)
    monkeypatch.setattr("sys.argv", ["generate.py"])  # no --rebuild-xls: customers.xls is committed as it is
    generate.main()
    built = sorted(p.name for p in tmp_path.iterdir())
    assert "customers.xls" not in built
    for name in built:
        if name.endswith(".xlsx"):
            # An Excel file is a zip, and each entry is stamped with the time it was written, so the bytes
            # differ from run to run. The cell contents are what must match.
            assert workbook_cells(tmp_path / name) == workbook_cells(DATA / name), f"{name} changed when regenerated"
        else:
            assert (tmp_path / name).read_bytes() == (DATA / name).read_bytes(), f"{name} changed when regenerated"


# ---------------------------------------------------------------------------
# Bad files fail in the way their names say
# ---------------------------------------------------------------------------


def test_utf8_bom_file_starts_with_the_byte_order_mark():
    assert (DATA / "customers-utf8-bom.csv").read_bytes().startswith(b"\xef\xbb\xbf")


def test_windows_1252_file_is_not_valid_utf8():
    raw = (DATA / "customers-windows-1252.csv").read_bytes()
    with pytest.raises(UnicodeDecodeError):
        raw.decode("utf-8")
    assert "Renée".encode("cp1252") in raw


def test_mixed_line_endings_has_both_crlf_and_lf():
    raw = (DATA / "customers-mixed-line-endings.csv").read_bytes()
    assert b"\r\n" in raw
    assert raw.replace(b"\r\n", b"").count(b"\n") > 0


def test_json_under_a_csv_name_parses_as_json():
    text = read_text("customers-as-json.csv")
    assert json.loads(text)[0]["customer_id"] == CUSTOMER_IDS[0]


def test_ragged_csv_has_rows_of_different_lengths():
    with open(DATA / "customers-ragged.csv", encoding="utf-8", newline="") as handle:
        counts = {len(row) for row in csv.reader(handle)}
    assert len(counts) > 1


def test_formula_csv_has_a_cell_starting_with_equals():
    rows = read_csv("customers-formula.csv")
    assert any(value.startswith("=") for row in rows for value in row.values())


def test_embedded_newline_csv_keeps_twelve_records():
    with open(DATA / "customers-embedded-newline.csv", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == len(CUSTOMERS)
    assert "\n" in rows[0]["address_street"]


def test_bad_dates_fail_on_three_rows():
    rows = read_csv("customers-bad-dates.csv")
    failures = []
    for row in rows:
        try:
            dt.date.fromisoformat(row["signup_date"])
        except ValueError:
            failures.append(row["signup_date"])
    assert failures == ["14/03/2021", "March 14, 2021", "2021-02-30"]


def test_duplicates_file_has_a_changed_repeat_and_an_exact_repeat():
    rows = read_csv("customers-duplicates.csv")
    counts = Counter(row["customer_id"] for row in rows)
    assert counts["1003"] == 2
    assert counts["1007"] == 2
    balances = {row["balance"] for row in rows if row["customer_id"] == "1003"}
    assert balances == {"980.10", "1100.00"}


def test_truncated_json_does_not_parse():
    with pytest.raises(json.JSONDecodeError):
        json.loads(read_text("customers-truncated.json"))


def test_big_numbers_lose_precision_as_floats():
    data = json.loads(read_text("customers-big-numbers.json"))
    for record in data:
        big = record["customer_id"]
        assert big > 2**53
        assert int(float(big)) != big


def test_null_mix_has_null_empty_and_missing_values():
    data = json.loads(read_text("customers-null-mix.json"))
    assert data[0]["email"] is None
    assert data[1]["name"] == ""
    assert data[1]["tags"] is None
    assert "email" not in data[2]


def test_orders_lines_has_exactly_one_malformed_line():
    lines = read_text("orders-lines.jsonl").splitlines()
    bad = []
    for number, line in enumerate(lines, start=1):
        try:
            json.loads(line)
        except json.JSONDecodeError:
            bad.append(number)
    assert bad == [7]


def test_fixed_short_row_is_shorter_than_the_layout():
    lines = read_text("customers-fixed-short-row.fixed").splitlines()
    assert len(lines[2]) < 56
    assert all(len(line) >= 56 for index, line in enumerate(lines) if index != 2)


def test_xxe_file_declares_an_external_entity():
    text = read_text("orders-xxe.xml")
    assert '<!ENTITY secret SYSTEM "file:///' in text


def test_norway_yaml_reads_no_and_on_as_booleans():
    data = yaml.safe_load(read_text("config-norway.yaml"))
    assert data["countries"][0]["code"] is False
    assert data["settings"]["notifications"] is True


def test_tab_indented_yaml_is_refused():
    with pytest.raises(yaml.YAMLError):
        yaml.safe_load(read_text("config-yaml-tabs.yaml"))


def test_text_numbers_xlsx_stores_numbers_as_text():
    sheet = openpyxl.load_workbook(DATA / "customers-text-numbers.xlsx")["customers"]
    assert isinstance(sheet.cell(row=2, column=1).value, str)
    assert isinstance(sheet.cell(row=2, column=5).value, str)


def test_formula_xlsx_has_a_formula_cell():
    sheet = openpyxl.load_workbook(DATA / "customers-formula.xlsx")["customers"]
    assert sheet.cell(row=2, column=2).value.startswith("=HYPERLINK")
