# Grouping Rows

A grouping collects the rows that share a key, and reports something about each group. This sample groups the orders by their `status`, and counts the orders in each group. The statuses are printed in a fixed order, so the output is the same in every language, and the order is the order a person would read them in.

The check is the total. The four group counts must add back up to the number of orders, which is twenty-four. A group that is missing from the list, or a status that matches no group, shows up as a difference in that total. A grouping that drops a row without a trace is one of the quiet mistakes this chapter is about, and the total is what catches it.

The key is compared exactly. A status with a trailing space would form its own group, and the count for `paid` would be one short. The check that the total matches is also the check that every row landed in one of the groups.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package CsvHelper@33.1.0

// The sample file is read from the folder named by TRAINING_DATA. The orders are grouped by status, and the groups are counted.
using System.Globalization;
using CsvHelper;
using CsvHelper.Configuration;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "orders.csv");
var rows = new List<string[]>();
using (var csv = new CsvReader(new StreamReader(path, System.Text.Encoding.UTF8), new CsvConfiguration(CultureInfo.InvariantCulture)))
{
    while (csv.Read())
    {
        rows.Add(csv.Parser.Record);
    }
}
var status = Array.IndexOf(rows[0], "status");
var counts = rows.Skip(1).GroupBy(row => row[status]).ToDictionary(group => group.Key, group => group.Count());
// Inline data, not from a sample file. The statuses in the order a reader expects them.
var order = new[] { "pending", "paid", "shipped", "refunded" };
foreach (var name in order)
{
    Console.WriteLine($"{char.ToUpperInvariant(name[0]) + name.Substring(1)}: {counts.GetValueOrDefault(name)}");
}
Console.WriteLine($"Total orders: {counts.Values.Sum()}");
```
```python
import csv
import os
from collections import Counter

# The sample file is read from the folder named by TRAINING_DATA. The orders are grouped by status, and the groups are counted.
path = os.path.join(os.environ["TRAINING_DATA"], "orders.csv")
with open(path, encoding="utf-8", newline="") as handle:
    orders = list(csv.DictReader(handle))
counts = Counter(order["status"] for order in orders)
# Inline data, not from a sample file. The statuses in the order a reader expects them.
for name in ["pending", "paid", "shipped", "refunded"]:
    print(f"{name.capitalize()}: {counts[name]}")
print(f"Total orders: {sum(counts.values())}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";
import { parse } from "csv-parse/sync";

// The sample file is read from the folder named by TRAINING_DATA. The orders are grouped by status, and the groups are counted.
const orders = parse(readFileSync(path.join(process.env.TRAINING_DATA, "orders.csv"), "utf8"), { columns: true });
const counts = new Map();
for (const order of orders) {
  counts.set(order.status, (counts.get(order.status) ?? 0) + 1);
}
// Inline data, not from a sample file. The statuses in the order a reader expects them.
for (const name of ["pending", "paid", "shipped", "refunded"]) {
  console.log(`${name[0].toUpperCase()}${name.slice(1)}: ${counts.get(name) ?? 0}`);
}
console.log(`Total orders: ${[...counts.values()].reduce((sum, count) => sum + count, 0)}`);
```
~~~

The output is the same in every language:

~~~text
Pending: 4
Paid: 9
Shipped: 8
Refunded: 3
Total orders: 24
~~~

The four groups add to 24, which is the number of orders in the file, so every row landed in a group. The count of a status that never appears is zero, not missing, because the output lists every status the reader expects. A status the reader did not expect would appear in the total and nowhere in the list, which is how the total exposes a new status in a feed.

> **Aside: a group is only as good as its key.**
> Grouping by `status` treats `Paid`, `paid`, and `paid ` as three different values. The key should be cleaned before the grouping, as the join will need in the next sample.

> **Common mistake.** Counting groups without checking the total. A grouping that loses rows still prints plausible counts, and only the sum of the counts shows the loss.

---
