# Formula Cells

CSV is plain text, so a CSV file can hold anything. Spreadsheets are the common reason a CSV file gets opened, and a spreadsheet treats a cell that begins with `=`, `+`, `-`, or `@` as a formula. A cell that reads `=HYPERLINK("https://example.invalid","Alice Carter")` becomes a live link when the file opens. A malicious file can do more: a formula can fetch data from elsewhere or, on some systems, run a command. The attack is called CSV injection, or formula injection, and it works because the reader of the file trusts the spreadsheet to show it as plain text.

The sample file `customers-formula.csv` holds one such cell. The first customer's name is a formula, not a name. Nothing in the parser stops it, because the parser correctly reads it as text. The parser's job is to report the cell, and the decision about what to do with it belongs to the program that writes or displays the file.

The sample below scans every field, and reports each one that starts with one of the four characters. It reports the line and the column, counting from one, and it doesn't change the data.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package CsvHelper@33.1.0

// The sample file is read from the folder named by TRAINING_DATA. Every field is checked for a leading formula character.
using System.Globalization;
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
var formulaChars = new[] { '=', '+', '-', '@' };
var found = 0;
for (var line = 0; line < rows.Count; line++)
{
    for (var column = 0; column < rows[line].Length; column++)
    {
        var value = rows[line][column];
        if (value.Length > 0 && formulaChars.Contains(value[0]))
        {
            found++;
            Console.WriteLine($"Line {line + 1}, column {column + 1} starts with {value[0]}");
        }
    }
}
Console.WriteLine($"Formula cells: {found}");
```
```python
import csv
import os

# The sample file is read from the folder named by TRAINING_DATA. Every field is checked for a leading formula character.
path = os.path.join(os.environ["TRAINING_DATA"], "customers-formula.csv")
formula_chars = "=+-@"
found = 0
with open(path, encoding="utf-8", newline="") as handle:
    reader = csv.reader(handle)
    for row in reader:
        for column, value in enumerate(row, start=1):
            if value and value[0] in formula_chars:
                found += 1
                print(f"Line {reader.line_num}, column {column} starts with {value[0]}")
print(f"Formula cells: {found}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";
import { parse } from "csv-parse/sync";

// The sample file is read from the folder named by TRAINING_DATA. Every field is checked for a leading formula character.
const rows = parse(readFileSync(path.join(process.env.TRAINING_DATA, "customers-formula.csv"), "utf8"));
const formulaChars = ["=", "+", "-", "@"];
let found = 0;
rows.forEach((row, line) => {
  row.forEach((value, column) => {
    if (value.length > 0 && formulaChars.includes(value[0])) {
      found++;
      console.log(`Line ${line + 1}, column ${column + 1} starts with ${value[0]}`);
    }
  });
});
console.log(`Formula cells: ${found}`);
```
~~~

The output is the same in every language:

~~~text
Line 2, column 2 starts with =
Formula cells: 1
~~~

The report names the line and column of the cell. Line two is the first customer, and column two is the name. The count is one, and it's the only cell in the file that starts with one of the four characters.

A detector like this is a check on input, not a fix. The usual defences, depending on the program, are to refuse the file, to report the cell, or to neutralize the value, most often by prefixing it with an apostrophe so the spreadsheet shows it as text. The sample reports only, because the choice belongs to the program that owns the data, and a silent change would alter the record.

> **Aside: a leading minus can be a real number.**
> A value such as `-45.00` is a legitimate amount, and a detector that flags every leading minus will report it. Detection of injection needs a rule about context, such as "a text field that starts with a formula character". The homework leaves that judgement to you.

> **Common mistake.** Assuming that a CSV file is safe because it's text. The parser is safe; the spreadsheet that opens it is the one that runs the formula, so the danger is in what the reader does next.

---
