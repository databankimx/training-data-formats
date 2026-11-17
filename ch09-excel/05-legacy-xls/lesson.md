# Legacy XLS

The file `customers.xls` holds the same customers and the same two sheets as `customers.xlsx`, in the legacy binary format. It starts with the OLE2 signature from Chapter 2, which the detector reports as `ole2`. The format stores each cell as a binary record, so the readers for the xlsx format, which work on zipped XML, can't open it.

Of the three libraries in this chapter, only the Python one reads the legacy format, through `xlrd`. ClosedXML and `exceljs` read only `.xlsx`. A C# or JavaScript program that receives a `.xls` file has to convert it first, with a tool outside these samples, or use a library that reads the legacy format. This is a limit of the libraries, not of the data, and the lesson says so because the failure is easy to miss until the file arrives.

Another point: `xlrd` returns every number as a floating-point value, even a whole number such as an identifier. The sample converts the identifier back to an integer, so it prints as `1001` and not `1001.0`.

~~~examples
Only in Python. ClosedXML and exceljs read only .xlsx, so the C# and JavaScript versions of this sample are not shown.

```python
import os

import xlrd

# The sample file is read from the folder named by TRAINING_DATA. xlrd reads the legacy binary format, which openpyxl does not.
path = os.path.join(os.environ["TRAINING_DATA"], "customers.xls")
workbook = xlrd.open_workbook(path)
sheet = workbook.sheet_by_name("customers")
customer_id = int(sheet.cell_value(1, 0))
name = sheet.cell_value(1, 1)
balance = sheet.cell_value(1, 4)
print(f"Sheets: {', '.join(workbook.sheet_names())}")
print(f"Records: {sheet.nrows - 1}")
print(f"First customer: {customer_id} {name} {balance}")
```
~~~

The output is:

~~~text
Sheets: customers, orders
Records: 12
First customer: 1001 Alice Carter 1250.75
~~~

The output matches the `.xlsx` sample for the same customer, which is what the shared dataset is for. `nrows` counts the header row as well, so the record count is one less. The sample takes the header row's position as given, the same way the earlier samples skipped it.

The C# and JavaScript versions of this sample are not in this chapter, for the reason above. The chapter's lessons don't pretend otherwise, and a learner who needs the legacy format in C# or JavaScript should convert the file to `.xlsx` first, or read it through a library that supports the binary records.

> **Aside: the detector knows more than the reader.**
> Chapter 2's detector reports `ole2` for this file, and it can't say whether the file is a workbook or a Word document. The reader is the step that decides, and a reader that is given the wrong file fails at that point.

> **Common mistake.** Renaming a `.xls` file to `.xlsx` to make a library accept it. The rename doesn't change the bytes, so the library still refuses the file. Convert the format, or read it with a reader for that format.

---
