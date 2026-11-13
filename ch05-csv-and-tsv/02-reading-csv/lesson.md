# Reading CSV

Reading CSV means turning the text into rows of fields, then treating the first row as the header. The parser has to follow the quoting rules from the first step: a comma inside quotes is ordinary text, and a comma outside quotes ends a field.

The sample below reads `customers.csv`, skips the header, and prints the count, the first customer, and the second customer. The second customer's name is `Okafor, Chidi`. A naive split would cut that name in two, so the third line of output is the check that the reader follows the quotes.

Each language uses a library for the parsing. You don't write the quote rules yourself: the library owns them, and the sample shows what it returns.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package CsvHelper@33.1.0

// The sample file is read from the folder named by TRAINING_DATA. CsvHelper follows the quoting rules.
using System.Globalization;
using CsvHelper;
using CsvHelper.Configuration;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers.csv");
using var reader = new StreamReader(path, System.Text.Encoding.UTF8);
using var csv = new CsvReader(reader, new CsvConfiguration(CultureInfo.InvariantCulture));
var rows = new List<string[]>();
while (csv.Read())
{
    rows.Add(csv.Parser.Record);
}
var records = rows.Skip(1).ToList();
Console.WriteLine($"Records: {records.Count}");
Console.WriteLine($"First customer: {records[0][0]} {records[0][1]}");
Console.WriteLine($"Second customer: {records[1][1]}");
```
```python
import csv
import os

# The sample file is read from the folder named by TRAINING_DATA. The csv module follows the quoting rules.
path = os.path.join(os.environ["TRAINING_DATA"], "customers.csv")
with open(path, encoding="utf-8", newline="") as handle:
    rows = list(csv.reader(handle))
records = rows[1:]
print(f"Records: {len(records)}")
print(f"First customer: {records[0][0]} {records[0][1]}")
print(f"Second customer: {records[1][1]}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";
import { parse } from "csv-parse/sync";

// The sample file is read from the folder named by TRAINING_DATA. csv-parse follows the quoting rules.
const table = parse(readFileSync(path.join(process.env.TRAINING_DATA, "customers.csv"), "utf8"));
const records = table.slice(1);
console.log(`Records: ${records.length}`);
console.log(`First customer: ${records[0][0]} ${records[0][1]}`);
console.log(`Second customer: ${records[1][1]}`);
```
~~~

The output is the same in every language:

~~~text
Records: 12
First customer: 1001 Alice Carter
Second customer: Okafor, Chidi
~~~

The three versions have the same shape: read the rows, drop the header, and index the fields. The C# version uses CsvHelper's reader, and the JavaScript version uses `csv-parse`, which is the Node library the `samples` folder declares. The Python version uses the standard `csv` module. Each one returns the same fields, because the quoting rules are the library's job, not yours.

The C# sample also needs the `#:package` line. A file-based C# program declares its NuGet packages at the top of the file, and the runner restores them the first time the file runs. That first run needs a network connection; later runs use the copy on the machine.

The values are text. The identifier `1001` comes out as the string `"1001"`, and the reader decides whether to turn it into a number. The chapter on JSON made the same point about types, and CSV has no types at all.

> **Aside: the header is data, too.**
> The first row names the columns, and a reader that uses the names rather than the positions survives a column being added. The samples here use positions, which is simpler, and the schema chapter returns to names.

> **Common mistake.** Forgetting to skip the header and counting it as a record. The count is then one too high, and the first customer is the column names. Decide the header's position once, and skip it.

---
