# Quoting and Newlines

A quoted field can hold a line break, and a reader that splits the file on line breaks will split the record in two. The file `customers-embedded-newline.csv` has a street address written on two lines inside one quoted field, for the first customer. It has twelve records and fourteen physical lines, so the two counts differ.

The sample below reads the file, counts the records, and counts the physical lines, which is the number of line feeds in the file. It then prints the first customer's street. The line break is shown as `<NL>`, so the output stays on one line and the break is still visible. The library does the quoting, and the physical line count comes from the text itself.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package CsvHelper@33.1.0

// The sample file is read from the folder named by TRAINING_DATA. CsvHelper keeps a quoted line break inside its field.
using System.Globalization;
using CsvHelper;
using CsvHelper.Configuration;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers-embedded-newline.csv");
var content = File.ReadAllText(path, System.Text.Encoding.UTF8);
var rows = new List<string[]>();
using (var csv = new CsvReader(new StringReader(content), new CsvConfiguration(CultureInfo.InvariantCulture)))
{
    while (csv.Read())
    {
        rows.Add(csv.Parser.Record);
    }
}
var records = rows.Skip(1).ToList();
var physicalLines = content.Count(c => c == '\n');
var street = records[0][7].Replace("\n", "<NL>");
Console.WriteLine($"Records: {records.Count}");
Console.WriteLine($"Physical lines: {physicalLines}");
Console.WriteLine($"Street of 1001: {street}");
```
```python
import csv
import os

# The sample file is read from the folder named by TRAINING_DATA. The csv module keeps a quoted line break inside its field.
path = os.path.join(os.environ["TRAINING_DATA"], "customers-embedded-newline.csv")
with open(path, encoding="utf-8", newline="") as handle:
    text = handle.read()
records = list(csv.reader(text.splitlines(keepends=True)))[1:]
physical_lines = text.count("\n")
street = records[0][7].replace("\n", "<NL>")
print(f"Records: {len(records)}")
print(f"Physical lines: {physical_lines}")
print(f"Street of 1001: {street}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";
import { parse } from "csv-parse/sync";

// The sample file is read from the folder named by TRAINING_DATA. csv-parse keeps a quoted line break inside its field.
const text = readFileSync(path.join(process.env.TRAINING_DATA, "customers-embedded-newline.csv"), "utf8");
const records = parse(text).slice(1);
const physicalLines = text.split("\n").length - 1;
const street = records[0][7].replaceAll("\n", "<NL>");
console.log(`Records: ${records.length}`);
console.log(`Physical lines: ${physicalLines}`);
console.log(`Street of 1001: ${street}`);
```
~~~

The output is the same in every language:

~~~text
Records: 12
Physical lines: 14
Street of 1001: 12 Maple<NL>Street
~~~

Twelve records, fourteen lines. The header is one line, the twelve records take thirteen, and the first customer's street adds the extra line. A tool that counts lines to estimate the number of records would report thirteen, and the reader would be wrong by one. The count of records is what the library returns, and it is the number a program should use.

The physical count is a different question, and it's the one a line-based tool answers. The library knows the quoted line break belongs to one field, so the records are right whatever the line count says.

> **Aside: why a line count is a lie.**
> A line feed is a fact about the bytes. A record is a fact about the structure. The two agree only when no field holds a line break, and a file that has never had one will mislead you the day it does.

> **Common mistake.** Reading the file with `readline` in a loop, and treating each line as a record. The first quoted newline turns one record into two broken ones, and both halves pass as records until the field count is checked.

---
