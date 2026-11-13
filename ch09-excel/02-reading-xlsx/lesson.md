# Reading XLSX

Reading a workbook starts with opening it, listing its sheets, and choosing one by name. The sample below opens `customers.xlsx`, lists its sheets, and reads the first customer from the `customers` sheet. It reads the stored values: the identifier is the number 1001, and the balance is the number 1250.75, which is what the file holds, whatever the display shows.

The first row is the header, so the sample starts at the second row. The three languages use different calls for the same job, and the output is the same.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package ClosedXML@0.105.1

// The sample file is read from the folder named by TRAINING_DATA. Cells are read as the numbers they store.
using ClosedXML.Excel;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers.xlsx");
using var workbook = new XLWorkbook(path);
var sheetNames = string.Join(", ", workbook.Worksheets.Select(sheet => sheet.Name));
var sheet = workbook.Worksheet("customers");
var rows = sheet.RowsUsed().Skip(1).ToList();
var first = rows[0];
var id = first.Cell(1).GetValue<double>();
var name = first.Cell(2).GetValue<string>();
var balance = first.Cell(5).GetValue<double>();
Console.WriteLine($"Sheets: {sheetNames}");
Console.WriteLine($"Records: {rows.Count}");
Console.WriteLine($"First customer: {id} {name} {balance}");
```
```python
import os

from openpyxl import load_workbook

# The sample file is read from the folder named by TRAINING_DATA. data_only returns the stored values, not the formulas.
path = os.path.join(os.environ["TRAINING_DATA"], "customers.xlsx")
workbook = load_workbook(path, data_only=True)
sheet = workbook["customers"]
rows = list(sheet.iter_rows(min_row=2, values_only=True))
first = rows[0]
print(f"Sheets: {', '.join(workbook.sheetnames)}")
print(f"Records: {len(rows)}")
print(f"First customer: {first[0]} {first[1]} {first[4]}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";
import ExcelJS from "exceljs";

// The sample file is read from the folder named by TRAINING_DATA. Cells are read as the values they store.
const workbook = new ExcelJS.Workbook();
await workbook.xlsx.readFile(path.join(process.env.TRAINING_DATA, "customers.xlsx"));
const sheet = workbook.getWorksheet("customers");
const rows = [];
sheet.eachRow((row, rowNumber) => {
  if (rowNumber > 1) rows.push(row);
});
const first = rows[0];
const id = first.getCell(1).value;
const name = first.getCell(2).value;
const balance = first.getCell(5).value;
console.log(`Sheets: ${workbook.worksheets.map((sheet) => sheet.name).join(", ")}`);
console.log(`Records: ${rows.length}`);
console.log(`First customer: ${id} ${name} ${balance}`);
```
~~~

The output is the same in every language:

~~~text
Sheets: customers, orders
Records: 12
First customer: 1001 Alice Carter 1250.75
~~~

Each library returns the stored number for the identifier and the balance, so the values print without any formatting. The sheet names come from the workbook part, and the rows come from the sheet part. The header row is skipped by starting one row down.

The three libraries use different indexing. ClosedXML and exceljs count columns from one, and openpyxl's `values_only` gives a tuple counted from zero. The code above keeps those differences visible, so a column that's off by one shows up at once.

Notice the `data_only=True` in the Python sample. Without it, openpyxl returns the formula for a formula cell, not its result. `customers.xlsx` has no formulas, so the difference doesn't show here, and the fourth sample depends on it.

> **Aside: the library reads the zip for you.**
> A workbook is a zip of XML, as the first step described. None of these samples unzips the file or parses the XML. The library does that, and the sample asks only for cells, which is the boundary a program should keep.

> **Common mistake.** Reading the balance from the display, such as by exporting the sheet to CSV and reading the text, and then wondering why `0` and `0.00` differ. Read the stored cell.

---
