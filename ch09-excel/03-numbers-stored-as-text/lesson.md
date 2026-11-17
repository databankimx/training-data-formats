# Numbers Stored as Text

A number can be stored as text in a workbook, and Excel shows the two almost identically. The cell's corner carries a small green triangle when the number is text, and that's the only visible sign. A sum over a range of text cells ignores them, and a formula that multiplies them may work or fail, depending on the function. A program reading the cell gets a string, not a number, and it has to decide what to do.

The file `customers-text-numbers.xlsx` stores the identifiers and the balances as text. The sample below reads the balances, counts how many are stored as text, and prints the first one with the type it has. Each library reports the stored type, and the check is the same in each.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package ClosedXML@0.105.1

// The sample file is read from the folder named by TRAINING_DATA. Each balance cell is checked for the type it stores.
using ClosedXML.Excel;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers-text-numbers.xlsx");
using var workbook = new XLWorkbook(path);
var sheet = workbook.Worksheet("customers");
var rows = sheet.RowsUsed().Skip(1).ToList();
var textBalances = rows.Count(row => row.Cell(5).DataType == XLDataType.Text);
var first = rows[0].Cell(5);
var firstType = first.DataType == XLDataType.Text ? "text" : "number";
Console.WriteLine($"Text balances: {textBalances}");
Console.WriteLine($"First customer balance: {first.GetString()} ({firstType})");
```
```python
import os

from openpyxl import load_workbook

# The sample file is read from the folder named by TRAINING_DATA. Each balance cell is checked for the type it stores.
path = os.path.join(os.environ["TRAINING_DATA"], "customers-text-numbers.xlsx")
workbook = load_workbook(path, data_only=True)
sheet = workbook["customers"]
balances = [row[4] for row in sheet.iter_rows(min_row=2, values_only=True)]
text_balances = sum(1 for value in balances if isinstance(value, str))
first = balances[0]
first_type = "text" if isinstance(first, str) else "number"
print(f"Text balances: {text_balances}")
print(f"First customer balance: {first} ({first_type})")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";
import ExcelJS from "exceljs";

// The sample file is read from the folder named by TRAINING_DATA. Each balance cell is checked for the type it stores.
const workbook = new ExcelJS.Workbook();
await workbook.xlsx.readFile(path.join(process.env.TRAINING_DATA, "customers-text-numbers.xlsx"));
const sheet = workbook.getWorksheet("customers");
const balances = [];
sheet.eachRow((row, rowNumber) => {
  if (rowNumber > 1) balances.push(row.getCell(5).value);
});
const textBalances = balances.filter((value) => typeof value === "string").length;
const first = balances[0];
const firstType = typeof first === "string" ? "text" : "number";
console.log(`Text balances: ${textBalances}`);
console.log(`First customer balance: ${first} (${firstType})`);
```
~~~

The output is the same in every language:

~~~text
Text balances: 12
First customer balance: 1250.75 (text)
~~~

Every balance in this file is text, and the first one prints the same digits as the number in the earlier sample. The difference is only in the type, and the type is what decides whether arithmetic works. A sum over these cells would give the wrong answer in Excel, and a sum in code needs each value converted first.

The check is on the stored type, not on the displayed text. The sample reads the cell's data type, not its contents, so a value that looks like a number but is stored as text is still caught.

> **Aside: the green triangle is the warning.**
> Excel marks text that looks like a number. If you see triangles on a column of numbers, the column is text, and the fix is in the source: export the number without quotes, or convert the cells before the sum.

> **Common mistake.** Converting text to numbers by reading it as a string and dropping the decimal point. Parse it with a decimal or float conversion, and check that the conversion succeeded.

---
