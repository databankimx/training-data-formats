# Formula Cells

A formula cell holds an expression rather than a value. In the file, the expression is stored with the cell, along with the value it last calculated. Excel recalculates formulas when a workbook opens, so a formula that reads a remote address or runs a command is a risk the moment the file is opened. The CSV formula injection in Chapter 5 is the same danger in a different format. A workbook from outside your system should be checked for formulas before anyone opens it in a spreadsheet.

The file `customers-formula.xlsx` has one formula. The name in the first customer's row is a `HYPERLINK` formula, not a name. The sample below scans every cell, counts the formulas, and reports the address of the first one. It doesn't print the formula text, because each library returns that text in a different form, and the address is the same everywhere.

The libraries must be told to read the formulas, not just the values. In the Python sample that is the default `data_only=False`, which is the opposite of the setting used in the second step.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package ClosedXML@0.105.1

// The sample file is read from the folder named by TRAINING_DATA. Every used cell is checked for a formula.
using ClosedXML.Excel;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers-formula.xlsx");
using var workbook = new XLWorkbook(path);
var sheet = workbook.Worksheet("customers");
var formulas = sheet.CellsUsed().Where(cell => cell.HasFormula).ToList();
Console.WriteLine($"Formula cells: {formulas.Count}");
Console.WriteLine($"First formula at: {formulas[0].Address}");
```
```python
import os

from openpyxl import load_workbook

# The sample file is read from the folder named by TRAINING_DATA. data_only is false, so formulas are read, not their results.
path = os.path.join(os.environ["TRAINING_DATA"], "customers-formula.xlsx")
workbook = load_workbook(path)
sheet = workbook["customers"]
formulas = [cell for row in sheet.iter_rows() for cell in row if isinstance(cell.value, str) and cell.value.startswith("=")]
print(f"Formula cells: {len(formulas)}")
print(f"First formula at: {formulas[0].coordinate}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";
import ExcelJS from "exceljs";

// The sample file is read from the folder named by TRAINING_DATA. Every cell is checked for a formula.
const workbook = new ExcelJS.Workbook();
await workbook.xlsx.readFile(path.join(process.env.TRAINING_DATA, "customers-formula.xlsx"));
const sheet = workbook.getWorksheet("customers");
const formulas = [];
sheet.eachRow((row) => {
  row.eachCell((cell) => {
    if (cell.type === ExcelJS.ValueType.Formula) formulas.push(cell);
  });
});
console.log(`Formula cells: ${formulas.length}`);
console.log(`First formula at: ${formulas[0].address}`);
```
~~~

The output is the same in every language:

~~~text
Formula cells: 1
First formula at: B2
~~~

The formula is in B2, the name column of the first customer. The count is one, because it's the only formula in the sheet. The address is the same whichever library reports it, so the output can be checked without comparing formula syntax.

The scan has to look at every cell, not just the columns that look suspicious. A formula can be placed in any cell, including one with a number in it, and a check on the column names would miss it.

> **Aside: a formula that looks like a value.**
> A formula's cached result is stored with it. A program reading only the result sees a plausible value, and the formula that would recalculate it is invisible. Read the formula flag, not just the value.

> **Common mistake.** Opening a workbook from outside in Excel to see what it contains. Excel will calculate its formulas as it opens, and a hostile formula runs on the reader's machine. Scan first, and open it in a sandbox if you must.

---
