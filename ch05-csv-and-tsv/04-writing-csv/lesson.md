# Writing CSV

Writing CSV means joining each row's fields with the delimiter, and quoting a field when it contains the delimiter, a quote, or a line break. A field with none of those is written as it is. A quote inside a quoted field is doubled. The rule is small, and it's where most hand-written CSV goes wrong, so the samples here let a library apply it.

The sample below writes three records, typed into the code. The second has a name with a comma, the third has a note with quotes in it, and the fourth has a note with a line break. The header and the first record need no quotes, and the others get exactly the quotes the rules require.

Each language has a writer. C# uses CsvHelper's `CsvWriter`, JavaScript uses `csv-stringify`, and Python uses the standard `csv` module's writer.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package CsvHelper@33.1.0

// Inline data, not from a sample file. Three records and a header, typed into the code, with a comma, quotes, and a line break among the values.
using System.Globalization;
using CsvHelper;
using CsvHelper.Configuration;
var rows = new List<string[]>
{
    new[] { "customer_id", "name", "note" },
    new[] { "1001", "Alice Carter", "plain" },
    new[] { "1002", "Okafor, Chidi", "says \"hi\"" },
    new[] { "1003", "Mei Lin", "two\nlines" },
};
using var csv = new CsvWriter(Console.Out, new CsvConfiguration(CultureInfo.InvariantCulture));
foreach (var row in rows)
{
    foreach (var value in row)
    {
        csv.WriteField(value);
    }
    csv.NextRecord();
}
csv.Flush();
```
```python
import csv
import sys

# Inline data, not from a sample file. Three records and a header, typed into the code, with a comma, quotes, and a line break among the values.
rows = [
    ["customer_id", "name", "note"],
    ["1001", "Alice Carter", "plain"],
    ["1002", "Okafor, Chidi", 'says "hi"'],
    ["1003", "Mei Lin", "two\nlines"],
]
writer = csv.writer(sys.stdout, lineterminator="\n")
writer.writerows(rows)
```
```javascript
import { stringify } from "csv-stringify/sync";

// Inline data, not from a sample file. Three records and a header, typed into the code, with a comma, quotes, and a line break among the values.
const rows = [
  ["customer_id", "name", "note"],
  ["1001", "Alice Carter", "plain"],
  ["1002", "Okafor, Chidi", 'says "hi"'],
  ["1003", "Mei Lin", "two\nlines"],
];
process.stdout.write(stringify(rows));
```
~~~

The output is the same in every language:

~~~text
customer_id,name,note
1001,Alice Carter,plain
1002,"Okafor, Chidi","says ""hi"""
1003,Mei Lin,"two
lines"
~~~

Look at the second record. The name is quoted because it contains a comma. The note is quoted because it contains quotes, and each of its quotes is doubled. The last record's note spans two lines, which is legal inside quotes. The header and the first record have no quotes at all, because nothing in them needed quoting. A writer that quotes everything is valid too, but it makes the file larger and harder to diff.

The rule has to apply to the header too. A column named `first, last` would need quotes in the header, and a reader that didn't expect that would split the name. The library applies the rule to every row, the header included, so you don't need a special case.

> **Aside: the writer must know the delimiter.**
> The writers here quote for the delimiter in use. A comma-separated file quotes a field that contains a comma, and a tab-separated file needs the opposite: a comma needs no quotes, and a tab does. Pass the delimiter to the writer, and the TSV sample at the end of the chapter shows the change.

> **Common mistake.** Adding quotes around every field by string concatenation, without doubling the quotes inside. A note of `says "hi"` becomes `"says "hi""`, which a reader closes early and then misreads. Let the writer apply the rule.

---
