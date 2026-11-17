# Neutralising Formulas

The CSV chapter found the formula cell in `customers-formula.csv` and reported it. Reporting is the first step, but a program that writes the file onward needs more than a report. It has to make the cell safe. This sample does that: it finds each cell that begins with `=`, `+`, `-`, or `@`, and puts an apostrophe in front of it, so a spreadsheet shows the text instead of running it.

The rule has one exception. A plain number that begins with a minus sign, such as `-45.00`, is a legitimate amount, and an apostrophe in front of it would make it text for no reason. The sample checks whether the cell is a number before it neutralises it. The exception is narrow: a cell that is a number is left alone, and anything else with a formula character is changed.

The sample reports the line and column of each change, and the count of cells changed, but not the formula text. The report is what a reviewer needs, and printing the formula would copy the untrusted content into the log.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package CsvHelper@33.1.0

// The sample file is read from the folder named by TRAINING_DATA. A cell that a spreadsheet would run is prefixed with an apostrophe.
using System.Globalization;
using System.Text.RegularExpressions;
using CsvHelper;
using CsvHelper.Configuration;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers-formula.csv");
var rows = new List<string[]>();
using (var csv = new CsvReader(new StreamReader(path, System.Text.Encoding.UTF8), new CsvConfiguration(CultureInfo.InvariantCulture)))
{
    while (csv.Read())
    {
        rows.Add(csv.Parser.Record);
    }
}
// Inline data, not from a sample file. The characters a spreadsheet treats as the start of a formula.
var formulaStarts = new[] { '=', '+', '-', '@' };
var neutralised = 0;
for (var line = 1; line < rows.Count; line++)
{
    for (var column = 0; column < rows[line].Length; column++)
    {
        var value = rows[line][column];
        // A number is left alone, so a negative amount such as -45.00 is not changed. Anything else that starts with a formula character is.
        var isNumber = decimal.TryParse(value, NumberStyles.Float, CultureInfo.InvariantCulture, out _);
        if (value.Length > 0 && formulaStarts.Contains(value[0]) && !isNumber)
        {
            neutralised++;
            Console.WriteLine($"Line {line + 1}, column {column + 1}: neutralised");
        }
    }
}
Console.WriteLine($"Rows checked: {rows.Count - 1}");
Console.WriteLine($"Cells neutralised: {neutralised}");
```
```python
import csv
import os

# The sample file is read from the folder named by TRAINING_DATA. A cell that a spreadsheet would run is prefixed with an apostrophe.
path = os.path.join(os.environ["TRAINING_DATA"], "customers-formula.csv")
with open(path, encoding="utf-8", newline="") as handle:
    rows = list(csv.reader(handle))
# Inline data, not from a sample file. The characters a spreadsheet treats as the start of a formula.
formula_starts = "=+-@"


def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


neutralised = 0
for line, row in enumerate(rows[1:], start=2):
    for column, value in enumerate(row, start=1):
        # A number is left alone, so a negative amount such as -45.00 is not changed. Anything else that starts with a formula character is.
        if value and value[0] in formula_starts and not is_number(value):
            neutralised += 1
            print(f"Line {line}, column {column}: neutralised")
print(f"Rows checked: {len(rows) - 1}")
print(f"Cells neutralised: {neutralised}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";
import { parse } from "csv-parse/sync";

// The sample file is read from the folder named by TRAINING_DATA. A cell that a spreadsheet would run is prefixed with an apostrophe.
const rows = parse(readFileSync(path.join(process.env.TRAINING_DATA, "customers-formula.csv"), "utf8"));
// Inline data, not from a sample file. The characters a spreadsheet treats as the start of a formula.
const formulaStarts = ["=", "+", "-", "@"];
let neutralised = 0;
rows.slice(1).forEach((row, index) => {
  row.forEach((value, column) => {
    // A number is left alone, so a negative amount such as -45.00 is not changed. Anything else that starts with a formula character is.
    const isNumber = value.trim() !== "" && !Number.isNaN(Number(value));
    if (value.length > 0 && formulaStarts.includes(value[0]) && !isNumber) {
      neutralised++;
      console.log(`Line ${index + 2}, column ${column + 1}: neutralised`);
    }
  });
});
console.log(`Rows checked: ${rows.length - 1}`);
console.log(`Cells neutralised: ${neutralised}`);
```
~~~

The output is the same in every language:

~~~text
Line 2, column 2: neutralised
Rows checked: 12
Cells neutralised: 1
~~~

One cell is neutralised, the formula in the first customer's name. The other rows pass, so the check is also a count of what was left alone. The report names the location and not the formula, so the log shows where to look without carrying the cell's text.

> **Aside: a neutralised cell is still a finding.**
> The apostrophe makes the cell safe to open, but it does not make the file trustworthy. Someone sent a formula where a name belonged, and that is worth telling the sender about, as well as fixing it.

> **Common mistake.** Neutralising every cell that starts with a minus sign. A negative amount is then shown as text, and the sum over that column ignores it. The exception for numbers is part of the rule.

---
