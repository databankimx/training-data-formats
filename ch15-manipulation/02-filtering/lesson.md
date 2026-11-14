# Filtering Rows

A filter keeps the rows that match a condition. This sample reads `orders.csv` and keeps the orders whose status is `paid`. It counts them and totals their amounts. The amounts are text in the file, so each one is converted to an exact decimal before it is added, and the total is printed with two places.

The condition compares the status exactly. A status of `Paid` or ` paid`, with a capital letter or a space, would not match, and the filter would drop the row without a warning. The samples in this tutorial have clean statuses, so the exact comparison is right here. A file with messy statuses should be cleaned first, as Chapter 12 showed.

The total is 4103.45, the same paid total the JSON Lines chapter found in the same orders, so the filter can be checked against that result.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package CsvHelper@33.1.0

// The sample file is read from the folder named by TRAINING_DATA. The rows whose status is paid are kept and totalled.
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
var header = rows[0];
string Value(string[] row, string column) => row[Array.IndexOf(header, column)];
var paid = rows.Skip(1).Where(row => Value(row, "status") == "paid").ToList();
// decimal keeps each amount exact, so the total has no floating-point drift.
decimal total = 0;
foreach (var row in paid)
{
    total += decimal.Parse(Value(row, "amount"), CultureInfo.InvariantCulture);
}
var totalText = total.ToString("F2", CultureInfo.InvariantCulture);
Console.WriteLine($"Paid orders: {paid.Count}");
Console.WriteLine($"Paid total: {totalText}");
```
```python
import csv
import os
from decimal import Decimal

# The sample file is read from the folder named by TRAINING_DATA. The rows whose status is paid are kept and totalled.
path = os.path.join(os.environ["TRAINING_DATA"], "orders.csv")
with open(path, encoding="utf-8", newline="") as handle:
    orders = list(csv.DictReader(handle))
paid = [order for order in orders if order["status"] == "paid"]
# Decimal keeps each amount exact, so the total has no floating-point drift.
total = sum((Decimal(order["amount"]) for order in paid), Decimal("0"))
print(f"Paid orders: {len(paid)}")
print(f"Paid total: {total:.2f}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";
import { parse } from "csv-parse/sync";

// The sample file is read from the folder named by TRAINING_DATA. The rows whose status is paid are kept and totalled.
const orders = parse(readFileSync(path.join(process.env.TRAINING_DATA, "orders.csv"), "utf8"), { columns: true });
const paid = orders.filter((order) => order.status === "paid");
// The amounts are summed in whole cents, so no binary float error builds up. The division happens once, at the end.
const cents = paid.reduce((sum, order) => sum + Math.round(Number(order.amount) * 100), 0);
console.log(`Paid orders: ${paid.length}`);
console.log(`Paid total: ${(cents / 100).toFixed(2)}`);
```
~~~

The output is the same in every language:

~~~text
Paid orders: 9
Paid total: 4103.45
~~~

Nine orders are paid, and they total 4103.45. The filter kept the rows whose status matched exactly, and the total used each amount's exact value. The amounts themselves are text, so the conversion to a decimal happens inside the sum, where a failure would show up as an error rather than as a wrong number.

> **Aside: a filter is a test on every row.**
> The condition runs on each row, and a row with an empty status fails the test. A filter that should have kept such a row needs its own rule, and the test should say what an empty value means.

> **Common mistake.** Testing the amount's text against a value such as `"0"` to find free orders. A text comparison says `"0.00"` is different from `"0"`, so the free orders are missed. Convert the amount first, and compare the number.

---
