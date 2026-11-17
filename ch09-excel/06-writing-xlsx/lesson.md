# Writing XLSX

Writing a workbook means creating a sheet, setting each cell's value, and saving the file. The value's type is what the cell stores. A number written as a number is stored as a number, and a boolean as a boolean. The sample below writes two customers and a header to a new workbook, saves it, and reopens it to check that the numbers and the boolean came back with their types.

The file is saved in the run folder, not in `samples\data`. Samples never write into the sample data, so a learner can run this step without changing the shared files.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package ClosedXML@0.105.1

// Inline data, not from a sample file. A header and two customers, typed into the code, with numbers and a boolean.
using ClosedXML.Excel;
using var workbook = new XLWorkbook();
var sheet = workbook.Worksheets.Add("customers");
sheet.Cell(1, 1).Value = "customer_id";
sheet.Cell(1, 2).Value = "name";
sheet.Cell(1, 3).Value = "balance";
sheet.Cell(1, 4).Value = "active";
sheet.Cell(2, 1).Value = 1001;
sheet.Cell(2, 2).Value = "Alice Carter";
sheet.Cell(2, 3).Value = 1250.75;
sheet.Cell(2, 4).Value = true;
sheet.Cell(3, 1).Value = 1002;
sheet.Cell(3, 2).Value = "Chidi Okafor";
sheet.Cell(3, 3).Value = 0.0;
sheet.Cell(3, 4).Value = false;
workbook.SaveAs("written-customers.xlsx");

// Reopen the saved file and read the balance back as a number.
using var reopened = new XLWorkbook("written-customers.xlsx");
var rows = reopened.Worksheet("customers").RowsUsed().Count();
var balance = reopened.Worksheet("customers").Cell(2, 3).GetValue<double>();
Console.WriteLine($"Rows read back: {rows}");
Console.WriteLine($"Balance in row 2: {balance}");
```
```python
from openpyxl import Workbook, load_workbook

# Inline data, not from a sample file. A header and two customers, typed into the code, with numbers and a boolean.
workbook = Workbook()
sheet = workbook.active
sheet.title = "customers"
sheet.append(["customer_id", "name", "balance", "active"])
sheet.append([1001, "Alice Carter", 1250.75, True])
sheet.append([1002, "Chidi Okafor", 0.0, False])
workbook.save("written-customers.xlsx")

# Reopen the saved file and read the balance back as a number.
reopened = load_workbook("written-customers.xlsx")
reopened_sheet = reopened["customers"]
rows = list(reopened_sheet.iter_rows(values_only=True))
print(f"Rows read back: {len(rows)}")
print(f"Balance in row 2: {reopened_sheet.cell(row=2, column=3).value}")
```
```javascript
import ExcelJS from "exceljs";

// Inline data, not from a sample file. A header and two customers, typed into the code, with numbers and a boolean.
const workbook = new ExcelJS.Workbook();
const sheet = workbook.addWorksheet("customers");
sheet.addRow(["customer_id", "name", "balance", "active"]);
sheet.addRow([1001, "Alice Carter", 1250.75, true]);
sheet.addRow([1002, "Chidi Okafor", 0, false]);
await workbook.xlsx.writeFile("written-customers.xlsx");

// Reopen the saved file and read the balance back as a number.
const reopened = new ExcelJS.Workbook();
await reopened.xlsx.readFile("written-customers.xlsx");
const reopenedSheet = reopened.getWorksheet("customers");
console.log(`Rows read back: ${reopenedSheet.rowCount}`);
console.log(`Balance in row 2: ${reopenedSheet.getCell(2, 3).value}`);
```
~~~

The output is the same in every language:

~~~text
Rows read back: 3
Balance in row 2: 1250.75
~~~

The header and the two customers come back as three rows, and the balance in row two is a number, so it prints without quotes. The saved file is a valid workbook that Excel opens, and the balance reads back as a number because that's what it was written as.

Writing a text value to a numeric column is the mistake the earlier step warned about. A balance written from a string such as `"1250.75"` is stored as text, so the write must convert values to numbers first. The samples here write numbers directly, which avoids the problem.

> **Aside: the file is recreated, not edited.**
> Each sample builds a new workbook and writes it over any file of the same name. Editing an existing workbook in place is a different operation, and the libraries handle it with separate calls.

> **Common mistake.** Writing a value and assuming Excel will display it as the program intended. The display format is set separately, so a balance of `0.0` shows as `0` unless a format is applied. Set the format where the display matters.

---
