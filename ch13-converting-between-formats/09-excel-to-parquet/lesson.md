# Excel to Parquet

This link reads `customers.xlsx` and writes `customers.parquet`. Both formats hold typed values, so the types should carry across without a guess. The identifier becomes a 64-bit integer, the active flag a boolean, and the text columns strings. The address and the tags are already flat columns in the workbook, so they stay flat in the Parquet file.

The balance is the important column. Parquet can store a decimal, so the C# and Python writers store it as a decimal with two places, and the value stays exact. The JavaScript writer used here stores the balance as a double, because its writer takes a type name for each column and this chain uses the plain one. A double holds `1250.75` as the nearest binary value, which is not exact. The chain's final check compares values, so the difference is visible only in a comparison that goes beyond two decimal places, and the lesson on Chapter 10 explained why exact decimals matter.

The output is the number of rows written.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package ClosedXML@0.105.1
#:package Parquet.Net@5.6.1

// The workbook is read from the chain folder, and each customer is written as a Parquet row for the next link to read.
using System.Globalization;
using ClosedXML.Excel;
using Parquet.Serialization;
var source = Path.Combine(Environment.GetEnvironmentVariable("CHAIN_DATA"), "customers.xlsx");
var target = Path.Combine(Environment.GetEnvironmentVariable("CHAIN_DATA"), "customers.parquet");
using var workbook = new XLWorkbook(source);
var rows = workbook.Worksheet("customers").RowsUsed().Skip(1).ToList();
var customers = rows.Select(row => new FlatCustomer
{
    customer_id = (long)row.Cell(1).GetValue<double>(),
    name = row.Cell(2).GetString(),
    email = row.Cell(3).GetString(),
    signup_date = row.Cell(4).GetString(),
    balance = decimal.Round((decimal)row.Cell(5).GetValue<double>(), 2),
    active = row.Cell(6).GetValue<bool>(),
    country_code = row.Cell(7).GetString(),
    address_street = row.Cell(8).GetString(),
    address_city = row.Cell(9).GetString(),
    address_postal_code = row.Cell(10).GetString(),
    tags = row.Cell(11).GetString(),
}).ToList();
await ParquetSerializer.SerializeAsync(customers, target);
Console.WriteLine($"Rows written: {customers.Count}");

class FlatCustomer
{
    public long customer_id { get; set; }
    public string name { get; set; } = "";
    public string email { get; set; } = "";
    public string signup_date { get; set; } = "";
    public decimal balance { get; set; }
    public bool active { get; set; }
    public string country_code { get; set; } = "";
    public string address_street { get; set; } = "";
    public string address_city { get; set; } = "";
    public string address_postal_code { get; set; } = "";
    public string tags { get; set; } = "";
}
```
```python
import os
from decimal import Decimal

import pyarrow as pa
import pyarrow.parquet as pq
from openpyxl import load_workbook

# The workbook is read from the chain folder, and each customer is written as a Parquet row for the next link to read.
source = os.path.join(os.environ["CHAIN_DATA"], "customers.xlsx")
target = os.path.join(os.environ["CHAIN_DATA"], "customers.parquet")
sheet = load_workbook(source, data_only=True)["customers"]
rows = list(sheet.iter_rows(min_row=2, values_only=True))
columns = {name: [] for name in ["customer_id", "name", "email", "signup_date", "balance", "active", "country_code", "address_street", "address_city", "address_postal_code", "tags"]}
for row in rows:
    columns["customer_id"].append(int(row[0]))
    columns["name"].append(row[1])
    columns["email"].append(row[2])
    columns["signup_date"].append(row[3])
    columns["balance"].append(Decimal(str(row[4])).quantize(Decimal("0.01")))
    columns["active"].append(bool(row[5]))
    columns["country_code"].append(row[6])
    columns["address_street"].append(row[7])
    columns["address_city"].append(row[8])
    columns["address_postal_code"].append(row[9])
    columns["tags"].append(row[10])
table = pa.table({
    "customer_id": pa.array(columns["customer_id"], type=pa.int64()),
    "name": columns["name"],
    "email": columns["email"],
    "signup_date": columns["signup_date"],
    "balance": pa.array(columns["balance"], type=pa.decimal128(10, 2)),
    "active": columns["active"],
    "country_code": columns["country_code"],
    "address_street": columns["address_street"],
    "address_city": columns["address_city"],
    "address_postal_code": columns["address_postal_code"],
    "tags": columns["tags"],
})
pq.write_table(table, target)
print(f"Rows written: {len(rows)}")
```
```javascript
import path from "node:path";
import ExcelJS from "exceljs";
import { parquetWriteFile } from "hyparquet-writer";

// The workbook is read from the chain folder, and each customer is written as a Parquet row for the next link to read.
const workbook = new ExcelJS.Workbook();
await workbook.xlsx.readFile(path.join(process.env.CHAIN_DATA, "customers.xlsx"));
const rows = [];
workbook.getWorksheet("customers").eachRow((row, rowNumber) => {
  if (rowNumber > 1) rows.push(row);
});
const column = (index, read) => rows.map((row) => read(row.getCell(index).value));
await parquetWriteFile({
  filename: path.join(process.env.CHAIN_DATA, "customers.parquet"),
  columnData: [
    { name: "customer_id", data: column(1, (value) => BigInt(value)), type: "INT64" },
    { name: "name", data: column(2, String), type: "STRING" },
    { name: "email", data: column(3, String), type: "STRING" },
    { name: "signup_date", data: column(4, String), type: "STRING" },
    { name: "balance", data: column(5, Number), type: "DOUBLE" },
    { name: "active", data: column(6, Boolean), type: "BOOLEAN" },
    { name: "country_code", data: column(7, String), type: "STRING" },
    { name: "address_street", data: column(8, String), type: "STRING" },
    { name: "address_city", data: column(9, String), type: "STRING" },
    { name: "address_postal_code", data: column(10, String), type: "STRING" },
    { name: "tags", data: column(11, String), type: "STRING" },
  ],
});
console.log(`Rows written: ${rows.length}`);
```
~~~

The output is the same in every language:

~~~text
Rows written: 12
~~~

Every column keeps its type through this link, except the balance in JavaScript, which becomes a double. The file has the same values in every language, and the chain's final comparison reads them back as numbers, so the difference only matters for arithmetic that needs exact cents.

> **Aside: a column's type is a promise to the reader.**
> A Parquet reader trusts the type it finds in the footer. A balance stored as a double is read as a double by every later tool, even though it was meant as money.

> **Common mistake.** Writing a balance as a double because the writer has a double type to hand. The result is nearly right, and the error appears only when two balances are added or compared exactly.

---
