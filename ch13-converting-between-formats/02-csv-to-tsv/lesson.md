# CSV to TSV

This is the first link of the conversion loop. The loop goes CSV, TSV, JSON, JSON Lines, XML, YAML, fixed-width, Excel, Parquet, and back to CSV, and every link reads the file the one before it wrote. This link reads `customers.csv` from the sample data, and writes the same rows as `customers.tsv` into the chain folder, which the runner provides as `CHAIN_DATA`.

The two formats hold the same rows. The change is the delimiter: a tab replaces the comma. A value that contains a comma, such as `Okafor, Chidi`, needs no quotes in TSV, so the writer doesn't add them. The tags stay as `vip;newsletter`, because the semicolon is text in both formats. Nothing is changed in form, so every fact is kept.

The output is the number of rows written. A later link reads the file this one writes, so run this step before the rest of the loop.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package CsvHelper@33.1.0

// The source is read from the sample data, and the TSV is written to the chain folder for the next link to read.
using System.Globalization;
using CsvHelper;
using CsvHelper.Configuration;
var source = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers.csv");
var target = Path.Combine(Environment.GetEnvironmentVariable("CHAIN_DATA"), "customers.tsv");
var rows = new List<string[]>();
using (var reader = new CsvReader(new StreamReader(source, System.Text.Encoding.UTF8), new CsvConfiguration(CultureInfo.InvariantCulture)))
{
    while (reader.Read())
    {
        rows.Add(reader.Parser.Record);
    }
}
using (var writer = new CsvWriter(new StreamWriter(target, false, new System.Text.UTF8Encoding(false)), new CsvConfiguration(CultureInfo.InvariantCulture) { Delimiter = "\t" }))
{
    foreach (var row in rows)
    {
        foreach (var value in row)
        {
            writer.WriteField(value);
        }
        writer.NextRecord();
    }
}
Console.WriteLine($"Rows written: {rows.Count - 1}");
```
```python
import csv
import os

# The source is read from the sample data, and the TSV is written to the chain folder for the next link to read.
source = os.path.join(os.environ["TRAINING_DATA"], "customers.csv")
target = os.path.join(os.environ["CHAIN_DATA"], "customers.tsv")
with open(source, encoding="utf-8", newline="") as handle:
    rows = list(csv.reader(handle))
with open(target, "w", encoding="utf-8", newline="") as handle:
    csv.writer(handle, delimiter="\t", lineterminator="\n").writerows(rows)
print(f"Rows written: {len(rows) - 1}")
```
```javascript
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { parse } from "csv-parse/sync";
import { stringify } from "csv-stringify/sync";

// The source is read from the sample data, and the TSV is written to the chain folder for the next link to read.
const rows = parse(readFileSync(path.join(process.env.TRAINING_DATA, "customers.csv"), "utf8"));
writeFileSync(path.join(process.env.CHAIN_DATA, "customers.tsv"), stringify(rows, { delimiter: "\t" }), "utf8");
console.log(`Rows written: ${rows.length - 1}`);
```
~~~

The output is the same in every language:

~~~text
Rows written: 12
~~~

The count is the number of data rows, not counting the header, which is written along with the rest. The file itself is the result that matters. The next link reads it, so a value that changed here would change every later link.

> **Aside: each link reads the previous file, not the sample.**
> A link that read `customers.csv` directly would skip everything the earlier links did. The chain only tests the formats if each link starts from the output of the one before.

> **Common mistake.** Writing the TSV with the default newline of the platform. A file written with Windows line endings is read correctly by most tools, but a comparison of the bytes will fail. The samples set the line ending explicitly.

---
