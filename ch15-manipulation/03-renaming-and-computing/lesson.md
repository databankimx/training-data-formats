# Renaming and Computing

A rename changes what a field is called, and the values stay as they were. A computation adds a value that comes from others. This sample does both to `customers.csv`. It renames `customer_id` to `id` and `name` to `full_name`, and it adds a `balance_cents` value for each customer, which is the balance multiplied by one hundred and held as a whole number.

The computation is the part to check. A balance in cents is exact only when it is computed with an exact type, because a float multiplied by one hundred can give a value such as `125074.99999999999`, which is not a whole number of cents. The sample uses decimals in C# and Python, and rounds the product of the number in JavaScript, where the binary float is the only type available.

The total of the cents is 1131180, which is the same balance total the earlier chapters found, in whole cents. A computed column is a claim about the data, so the total is the check that the computation did what it says.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package CsvHelper@33.1.0

// The sample file is read from the folder named by TRAINING_DATA. Columns are renamed, and each balance is computed in cents.
using System.Globalization;
using CsvHelper;
using CsvHelper.Configuration;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers.csv");
var rows = new List<string[]>();
using (var csv = new CsvReader(new StreamReader(path, System.Text.Encoding.UTF8), new CsvConfiguration(CultureInfo.InvariantCulture)))
{
    while (csv.Read())
    {
        rows.Add(csv.Parser.Record);
    }
}
var header = rows[0];
string Value(string[] row, string column) => row[Array.IndexOf(header, column)];
var renamed = rows.Skip(1).Select(row => new
{
    id = Value(row, "customer_id"),
    full_name = Value(row, "name"),
    balance_cents = (long)(decimal.Parse(Value(row, "balance"), CultureInfo.InvariantCulture) * 100m),
}).ToList();
var first = renamed[0];
Console.WriteLine($"Renamed record: id={first.id} full_name={first.full_name}");
Console.WriteLine($"Alice balance in cents: {first.balance_cents}");
Console.WriteLine($"Total balance in cents: {renamed.Sum(record => record.balance_cents)}");
```
```python
import csv
import os
from decimal import Decimal

# The sample file is read from the folder named by TRAINING_DATA. Columns are renamed, and each balance is computed in cents.
path = os.path.join(os.environ["TRAINING_DATA"], "customers.csv")
with open(path, encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle))
renamed = [
    {
        "id": row["customer_id"],
        "full_name": row["name"],
        "balance_cents": int(Decimal(row["balance"]) * 100),
    }
    for row in rows
]
first = renamed[0]
print(f"Renamed record: id={first['id']} full_name={first['full_name']}")
print(f"Alice balance in cents: {first['balance_cents']}")
print(f"Total balance in cents: {sum(record['balance_cents'] for record in renamed)}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";
import { parse } from "csv-parse/sync";

// The sample file is read from the folder named by TRAINING_DATA. Columns are renamed, and each balance is computed in cents.
const rows = parse(readFileSync(path.join(process.env.TRAINING_DATA, "customers.csv"), "utf8"), { columns: true });
const renamed = rows.map((row) => ({
  id: row.customer_id,
  full_name: row.name,
  balance_cents: Math.round(Number(row.balance) * 100),
}));
const first = renamed[0];
console.log(`Renamed record: id=${first.id} full_name=${first.full_name}`);
console.log(`Alice balance in cents: ${first.balance_cents}`);
console.log(`Total balance in cents: ${renamed.reduce((sum, record) => sum + record.balance_cents, 0)}`);
```
~~~

The output is the same in every language:

~~~text
Renamed record: id=1001 full_name=Alice Carter
Alice balance in cents: 125075
Total balance in cents: 1131180
~~~

The rename changed only the names, and the first record keeps its values. The balance of 1250.75 is 125075 cents, a whole number, and the total is 1131180 cents, which is 11311.80. The JavaScript version rounds the product to the nearest whole cent, so a product that is a little off in binary still lands on the right whole number.

> **Aside: a rename is a change to the contract.**
> Any program that reads the old names breaks when the names change. A rename belongs in the same place as the schema, so the two stay in step.

> **Common mistake.** Truncating a computed value with a float conversion, such as `int(balance * 100)`. A float of `1250.75 * 100` can land just below `125075`, and the truncation drops a cent. Round first, or compute with an exact type.

---
