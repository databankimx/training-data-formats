# Fixed-Width to Excel

This link reads `customers.fixed` by position, using the layout from the previous link, and writes `customers.xlsx`. The reading is the Chapter 6 work, with more fields. The writing is where the types matter. The identifier and the balance are written as numbers, the active flag as a boolean, and the postal code as text, so its leading zero survives. The tags and the email are text.

The balance is the loss to watch. A balance of `0.00` is written as the number zero, and a reader of the workbook sees `0`, not `0.00`. The value is still zero, and the text is different. The final link of the chain writes the balance with two decimal places again, so the text comes back. A chain that didn't do that would fail the text check, and the lesson on that check explains why it matters.

The output is the number of rows written, not counting the header.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package ClosedXML@0.105.1

// The fixed-width file is read by position, and each customer is written to a workbook in the chain folder for the next link.
using System.Globalization;
using ClosedXML.Excel;
var source = Path.Combine(Environment.GetEnvironmentVariable("CHAIN_DATA"), "customers.fixed");
var target = Path.Combine(Environment.GetEnvironmentVariable("CHAIN_DATA"), "customers.xlsx");
var lines = File.ReadAllLines(source, System.Text.Encoding.UTF8);
// Inline data, not from a sample file. The start position of each field, counted from zero, and its width.
using var workbook = new XLWorkbook();
var sheet = workbook.Worksheets.Add("customers");
var header = new[] { "customer_id", "name", "email", "signup_date", "balance", "active", "country_code", "address_street", "address_city", "address_postal_code", "tags" };
for (var column = 0; column < header.Length; column++)
{
    sheet.Cell(1, column + 1).Value = header[column];
}
var row = 2;
foreach (var line in lines)
{
    sheet.Cell(row, 1).Value = double.Parse(line.Substring(0, 6).Trim(), CultureInfo.InvariantCulture);
    sheet.Cell(row, 2).Value = line.Substring(7, 20).Trim();
    sheet.Cell(row, 3).Value = line.Substring(147, 32).Trim();
    sheet.Cell(row, 4).Value = line.Substring(28, 10).Trim();
    sheet.Cell(row, 5).Value = double.Parse(line.Substring(39, 8).Trim(), CultureInfo.InvariantCulture);
    sheet.Cell(row, 6).Value = line.Substring(48, 5).Trim() == "true";
    sheet.Cell(row, 7).Value = line.Substring(54, 2).Trim();
    sheet.Cell(row, 8).Value = line.Substring(57, 26).Trim();
    sheet.Cell(row, 9).Value = line.Substring(84, 20).Trim();
    sheet.Cell(row, 10).SetValue(line.Substring(105, 10).Trim());
    sheet.Cell(row, 11).Value = line.Substring(116, 30).Trim();
    row++;
}
workbook.SaveAs(target);
Console.WriteLine($"Rows written: {lines.Length}");
```
```python
import os

from openpyxl import Workbook

# The fixed-width file is read by position, and each customer is written to a workbook in the chain folder for the next link.
source = os.path.join(os.environ["CHAIN_DATA"], "customers.fixed")
target = os.path.join(os.environ["CHAIN_DATA"], "customers.xlsx")
with open(source, encoding="utf-8") as handle:
    lines = handle.read().splitlines()
workbook = Workbook()
sheet = workbook.active
sheet.title = "customers"
sheet.append(["customer_id", "name", "email", "signup_date", "balance", "active", "country_code", "address_street", "address_city", "address_postal_code", "tags"])
for line in lines:
    sheet.append([
        int(line[0:6].strip()),
        line[7:27].strip(),
        line[147:179].strip(),
        line[28:38].strip(),
        float(line[39:47].strip()),
        line[48:53].strip() == "true",
        line[54:56].strip(),
        line[57:83].strip(),
        line[84:104].strip(),
        line[105:115].strip(),
        line[116:146].strip(),
    ])
workbook.save(target)
print(f"Rows written: {len(lines)}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";
import ExcelJS from "exceljs";

// The fixed-width file is read by position, and each customer is written to a workbook in the chain folder for the next link.
const lines = readFileSync(path.join(process.env.CHAIN_DATA, "customers.fixed"), "utf8").split("\n").filter((line) => line !== "");
const workbook = new ExcelJS.Workbook();
const sheet = workbook.addWorksheet("customers");
sheet.addRow(["customer_id", "name", "email", "signup_date", "balance", "active", "country_code", "address_street", "address_city", "address_postal_code", "tags"]);
for (const line of lines) {
  sheet.addRow([
    Number(line.slice(0, 6).trim()),
    line.slice(7, 27).trim(),
    line.slice(147, 179).trim(),
    line.slice(28, 38).trim(),
    Number(line.slice(39, 47).trim()),
    line.slice(48, 53).trim() === "true",
    line.slice(54, 56).trim(),
    line.slice(57, 83).trim(),
    line.slice(84, 104).trim(),
    line.slice(105, 115).trim(),
    line.slice(116, 146).trim(),
  ]);
}
await workbook.xlsx.writeFile(path.join(process.env.CHAIN_DATA, "customers.xlsx"));
console.log(`Rows written: ${lines.length}`);
```
~~~

The output is the same in every language:

~~~text
Rows written: 12
~~~

The reads use the positions from the layout, counted from zero in code, and each value is trimmed. The postal code is written with `SetValue` in C#, which keeps it a string even though it looks like a number. In openpyxl and exceljs a string is written as a string already, so the postal code keeps its zeros in every language. The balance is written as a number, and the email is now a column of its own.

> **Aside: the cell type is the decision.**
> Excel stores what the writer gives it. A text value that looks like a number is kept as text only if it is written as text, which is why the postal code is written deliberately.

> **Common mistake.** Writing every value through a generic setter that guesses the type. A postal code such as `0155` then becomes the number 155, and the leading zero is gone from the file. Choose the cell type for each column.

---
