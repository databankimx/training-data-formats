# TSV

A TSV file is CSV with a tab as the delimiter. The same quoting rules apply, and the same reader works, with one change: the delimiter is a tab. The sample file `customers.tsv` holds the same twelve customers as `customers.csv`, so the two can be compared.

The change matters for quoting. In a TSV file, the second customer's name is `Okafor, Chidi`, with no quotes, because a comma is ordinary text there. The quotes are needed only when a value contains a tab, a quote, or a line break. A tab in a value is the hard case, since TSV has no standard way to escape one, and a file with a tab inside a value must be written with quotes or not at all.

The sample below reads `customers.tsv` with a tab delimiter. It counts the records and prints the second customer's name, which is the value that would need quotes in CSV and doesn't need them here.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package CsvHelper@33.1.0

// The sample file is read from the folder named by TRAINING_DATA. The same reader runs, with a tab as the delimiter.
using System.Globalization;
using CsvHelper;
using CsvHelper.Configuration;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers.tsv");
var config = new CsvConfiguration(CultureInfo.InvariantCulture) { Delimiter = "\t" };
var rows = new List<string[]>();
using (var csv = new CsvReader(new StreamReader(path, System.Text.Encoding.UTF8), config))
{
    while (csv.Read())
    {
        rows.Add(csv.Parser.Record);
    }
}
var records = rows.Skip(1).ToList();
Console.WriteLine($"Records: {records.Count}");
Console.WriteLine($"Second customer: {records[1][1]}");
```
```python
import csv
import os

# The sample file is read from the folder named by TRAINING_DATA. The same csv module runs, with a tab as the delimiter.
path = os.path.join(os.environ["TRAINING_DATA"], "customers.tsv")
with open(path, encoding="utf-8", newline="") as handle:
    records = list(csv.reader(handle, delimiter="\t"))[1:]
print(f"Records: {len(records)}")
print(f"Second customer: {records[1][1]}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";
import { parse } from "csv-parse/sync";

// The sample file is read from the folder named by TRAINING_DATA. The same parser runs, with a tab as the delimiter.
const records = parse(readFileSync(path.join(process.env.TRAINING_DATA, "customers.tsv"), "utf8"), {
  delimiter: "\t",
}).slice(1);
console.log(`Records: ${records.length}`);
console.log(`Second customer: ${records[1][1]}`);
```
~~~

The output is the same in every language:

~~~text
Records: 12
Second customer: Okafor, Chidi
~~~

The output matches the CSV sample for the same data, and the one value that differs in the file is the one that matters here. In `customers.csv` the name sits inside quotes, and in `customers.tsv` it doesn't. A reader that handles both needs no special case: the quoting rule is the same, and the delimiter decides where the fields end.

Notice what the reader does not do. It doesn't pick the delimiter from the file. A tab-separated file read with a comma delimiter would give one field per line, and the file's first line would look like a column name with tabs in it. The format has to be known, or detected by the method in Chapter 2.

> **Aside: why TSV is often preferred for text data.**
> Commas are common in names, addresses, and free text. Tabs almost never appear in those values, so a TSV file needs quoting far less often, and a reader that splits on tabs makes fewer mistakes. The trade-off is that a tab in a value is hard to represent at all.

> **Common mistake.** Opening a TSV file with a comma reader, and seeing one column of text that looks almost right. The file is intact; the reader is pointed at the wrong delimiter.

---
