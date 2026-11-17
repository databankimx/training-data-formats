# Removing Duplicates

The file `customers-duplicates.csv` has fourteen data rows, and two of them repeat an earlier customer. Line fifteen, customer 1007, is an exact copy of the original on line eight, so removing it loses nothing. Line fourteen, customer 1003, repeats the identifier with a different balance: 980.10 on the original and 1100.00 on the copy. The two rows disagree, so neither can be removed on the cleaner's judgement. Both stay in the data, and the later one is flagged.

A row is removed only when every field matches a row already kept. The cleaner compares the whole row, not the identifier alone, and it reports each decision on its own line. The totals are the rows kept, the rows removed, and the rows needing review. A conflict is not a removal, so the kept count includes it.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package CsvHelper@33.1.0

// The sample file is read from the folder named by TRAINING_DATA. A repeated row is removed only when every field matches.
using System.Linq;
using CsvHelper;
using CsvHelper.Configuration;
using System.Globalization;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers-duplicates.csv");
var rows = new List<string[]>();
using (var csv = new CsvReader(new StreamReader(path, System.Text.Encoding.UTF8), new CsvConfiguration(CultureInfo.InvariantCulture)))
{
    while (csv.Read())
    {
        rows.Add(csv.Parser.Record);
    }
}
var body = rows.Skip(1).ToList();
// Inline data, not from a sample file. The first copy of each identifier is the one kept.
var firstCopy = new Dictionary<string, string[]>();
var kept = 0;
var removed = 0;
var review = 0;
for (var index = 0; index < body.Count; index++)
{
    var row = body[index];
    var id = row[0];
    var line = index + 2;
    if (!firstCopy.TryGetValue(id, out var first))
    {
        firstCopy[id] = row;
        kept++;
    }
    else if (first.SequenceEqual(row))
    {
        removed++;
        Console.WriteLine($"Line {line}: customer_id {id} is an exact copy, removed");
    }
    else
    {
        kept++;
        review++;
        Console.WriteLine($"Line {line}: customer_id {id} has a conflicting copy, kept for review");
    }
}
Console.WriteLine($"Rows kept: {kept}");
Console.WriteLine($"Rows removed: {removed}");
Console.WriteLine($"Rows needing review: {review}");
```
```python
import csv
import os

# The sample file is read from the folder named by TRAINING_DATA. A repeated row is removed only when every field matches.
path = os.path.join(os.environ["TRAINING_DATA"], "customers-duplicates.csv")
with open(path, encoding="utf-8", newline="") as handle:
    body = list(csv.reader(handle))[1:]
# Inline data, not from a sample file. The first copy of each identifier is the one kept.
first_copy = {}
kept = 0
removed = 0
review = 0
for index, row in enumerate(body):
    customer_id = row[0]
    line = index + 2
    if customer_id not in first_copy:
        first_copy[customer_id] = row
        kept += 1
    elif first_copy[customer_id] == row:
        removed += 1
        print(f"Line {line}: customer_id {customer_id} is an exact copy, removed")
    else:
        kept += 1
        review += 1
        print(f"Line {line}: customer_id {customer_id} has a conflicting copy, kept for review")
print(f"Rows kept: {kept}")
print(f"Rows removed: {removed}")
print(f"Rows needing review: {review}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";
import { parse } from "csv-parse/sync";

// The sample file is read from the folder named by TRAINING_DATA. A repeated row is removed only when every field matches.
const body = parse(readFileSync(path.join(process.env.TRAINING_DATA, "customers-duplicates.csv"), "utf8")).slice(1);
// Inline data, not from a sample file. The first copy of each identifier is the one kept.
const firstCopy = new Map();
let kept = 0;
let removed = 0;
let review = 0;
body.forEach((row, index) => {
  const id = row[0];
  const line = index + 2;
  if (!firstCopy.has(id)) {
    firstCopy.set(id, row);
    kept++;
  } else if (JSON.stringify(firstCopy.get(id)) === JSON.stringify(row)) {
    removed++;
    console.log(`Line ${line}: customer_id ${id} is an exact copy, removed`);
  } else {
    kept++;
    review++;
    console.log(`Line ${line}: customer_id ${id} has a conflicting copy, kept for review`);
  }
});
console.log(`Rows kept: ${kept}`);
console.log(`Rows removed: ${removed}`);
console.log(`Rows needing review: ${review}`);
```
~~~

The output is the same in every language:

~~~text
Line 14: customer_id 1003 has a conflicting copy, kept for review
Line 15: customer_id 1007 is an exact copy, removed
Rows kept: 13
Rows removed: 1
Rows needing review: 1
~~~

Of the fourteen rows, thirteen are kept and one is removed. The conflict on line fourteen is kept, so a person can see both balances and decide which is right. The exact copy on line fifteen is removed, and its removal is recorded.

The comparison is on the whole row. A cleaner that compared only the identifiers would remove line fourteen, and it would discard a balance that may be the correct one. The rule is strict because the cost of a wrong removal is larger than the cost of a conflict left for review.

> **Aside: keep the first copy, but never let the rule decide a conflict.**
> Keeping the first copy is a convention, and it is the same convention for every duplicate. The conflict is different: both copies are kept, because only a person knows which is current.

> **Common mistake.** Removing duplicates before normalizing the values. Two copies that differ only by a trailing space look different, so they are kept, and after trimming they are identical. Clean first, then compare.

---
