# Ragged Rows

A ragged row is a record with a different number of fields from the header. CSV allows nothing else, so a ragged row is always a sign of damage: a field lost a comma, an extra comma slipped into a value without quotes, or an export wrote a column the header doesn't list. The file `customers-ragged.csv` has two. Line four lost its last field, and line seven gained one.

A reader has three choices, and only one is safe. It can pad or trim the row to match the header, which hides the problem and may put values in the wrong columns. It can stop, which is safe but throws away the good rows. Or it can report each ragged row by its line number, and let someone decide. The sample takes the third choice, because a guess about which field is missing can be wrong in a way nothing will show.

The sample below reads the file, takes the header's field count, and reports each row that differs from it. The line numbers count from one, and the header is line one, so a row's line number is its index plus one.

Some libraries refuse ragged rows by default, and that's a choice you can make on purpose. CsvHelper's raw record reader returns each row as it stands, and `csv-parse` needs `relax_column_count` to do the same. Both are set up that way here, so the damage reaches the report.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package CsvHelper@33.1.0

// The sample file is read from the folder named by TRAINING_DATA. Each row is compared with the header's field count.
using System.Globalization;
using CsvHelper;
using CsvHelper.Configuration;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers-ragged.csv");
var rows = new List<string[]>();
using (var csv = new CsvReader(new StreamReader(path, System.Text.Encoding.UTF8), new CsvConfiguration(CultureInfo.InvariantCulture)))
{
    while (csv.Read())
    {
        rows.Add(csv.Parser.Record);
    }
}
var expected = rows[0].Length;
Console.WriteLine($"Header fields: {expected}");
for (var i = 1; i < rows.Count; i++)
{
    if (rows[i].Length != expected)
    {
        Console.WriteLine($"Line {i + 1} has {rows[i].Length} fields");
    }
}
```
```python
import csv
import os

# The sample file is read from the folder named by TRAINING_DATA. Each row is compared with the header's field count.
path = os.path.join(os.environ["TRAINING_DATA"], "customers-ragged.csv")
with open(path, encoding="utf-8", newline="") as handle:
    reader = csv.reader(handle)
    header = next(reader)
    print(f"Header fields: {len(header)}")
    for row in reader:
        if len(row) != len(header):
            print(f"Line {reader.line_num} has {len(row)} fields")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";
import { parse } from "csv-parse/sync";

// The sample file is read from the folder named by TRAINING_DATA. Each row is compared with the header's field count.
const rows = parse(readFileSync(path.join(process.env.TRAINING_DATA, "customers-ragged.csv"), "utf8"), {
  relax_column_count: true,
});
const expected = rows[0].length;
console.log(`Header fields: ${expected}`);
for (let i = 1; i < rows.length; i++) {
  if (rows[i].length !== expected) {
    console.log(`Line ${i + 1} has ${rows[i].length} fields`);
  }
}
```
~~~

The output is the same in every language:

~~~text
Header fields: 11
Line 4 has 10 fields
Line 7 has 12 fields
~~~

The header has eleven fields. Line four has ten, because its tags field was lost, and line seven has twelve, because of the extra value appended to it. The report gives the line numbers, and a person can open the file at those lines and see what happened.

Notice the second customer's line. It has a quoted comma in the name, so a naive split would count it as twelve fields and report it as ragged. The library counts it correctly as eleven, so it isn't reported. A count that flags that line would be wrong in the other direction, and it's the quoting that makes the difference.

> **Aside: why report, not repair?**
> Repairing a ragged row means choosing which field is missing. In `customers-ragged.csv` the tags field of line four is the obvious guess, but the file doesn't say so, and the wrong guess would put a value into the wrong column without any sign.

> **Common mistake.** Counting fields by splitting on commas and comparing with the header. It flags every row with a quoted comma, which is most of the names in a file like this one.

---
