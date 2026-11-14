# Joining Customers and Orders

A join matches the rows of one table with the rows of another on a shared key. Here the key is `customer_id`, which appears in both `customers.csv` and `orders.csv`. This sample joins each order to its customer, then reports two things: which customers have no orders, and the orders of the customers in Norway, with their total.

The first report is a left join's check. The join starts from the customers and keeps every one of them, so a customer with no orders appears with an empty count rather than vanishing. An inner join would drop that customer silently. In this data every customer has at least one order, so the count is zero, and a count other than zero would mean a customer is missing from the orders, or an order refers to a customer id that does not exist.

The second report is a filter on the joined result. The orders of the Norwegian customer, Lars Haugen, are totalled exactly, and the total of 2575.50 is the sum of his three orders, which the grouping in the last sample would have counted in the `pending`, `paid`, and `shipped` groups.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package CsvHelper@33.1.0

// The sample files are read from the folder named by TRAINING_DATA. Orders are joined to customers on customer_id.
using System.Globalization;
using CsvHelper;
using CsvHelper.Configuration;
List<string[]> ReadRows(string file)
{
    var rows = new List<string[]>();
    using var csv = new CsvReader(new StreamReader(file, System.Text.Encoding.UTF8), new CsvConfiguration(CultureInfo.InvariantCulture));
    while (csv.Read())
    {
        rows.Add(csv.Parser.Record);
    }
    return rows;
}
var customerRows = ReadRows(Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers.csv"));
var orderRows = ReadRows(Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "orders.csv"));
var customerHeader = customerRows[0];
var orderHeader = orderRows[0];
var customers = customerRows.Skip(1).ToDictionary(row => row[Array.IndexOf(customerHeader, "customer_id")], row => row);
var ordersByCustomer = orderRows.Skip(1).GroupBy(row => row[Array.IndexOf(orderHeader, "customer_id")]).ToDictionary(group => group.Key, group => group.ToList());
var withoutOrders = customers.Keys.Count(id => !ordersByCustomer.ContainsKey(id));
Console.WriteLine($"Customers: {customers.Count}");
Console.WriteLine($"Customers with no orders: {withoutOrders}");
var norwegian = customers.Values.Where(row => row[Array.IndexOf(customerHeader, "country_code")] == "NO").ToList();
var norwegianOrders = norwegian.SelectMany(row => ordersByCustomer.GetValueOrDefault(row[0], new List<string[]>())).ToList();
// decimal keeps each amount exact, so the total has no floating-point drift.
decimal total = 0;
foreach (var row in norwegianOrders)
{
    total += decimal.Parse(row[Array.IndexOf(orderHeader, "amount")], CultureInfo.InvariantCulture);
}
Console.WriteLine($"Orders for NO customers: {norwegianOrders.Count}");
var totalText = total.ToString("F2", CultureInfo.InvariantCulture);
Console.WriteLine($"{norwegian[0][1]}: {norwegianOrders.Count} orders, total {totalText}");
```
```python
import csv
import os
from collections import defaultdict
from decimal import Decimal

# The sample files are read from the folder named by TRAINING_DATA. Orders are joined to customers on customer_id.
folder = os.environ["TRAINING_DATA"]
with open(os.path.join(folder, "customers.csv"), encoding="utf-8", newline="") as handle:
    customers = {row["customer_id"]: row for row in csv.DictReader(handle)}
with open(os.path.join(folder, "orders.csv"), encoding="utf-8", newline="") as handle:
    orders = list(csv.DictReader(handle))
orders_by_customer = defaultdict(list)
for order in orders:
    orders_by_customer[order["customer_id"]].append(order)
without_orders = sum(1 for customer_id in customers if customer_id not in orders_by_customer)
print(f"Customers: {len(customers)}")
print(f"Customers with no orders: {without_orders}")
norwegian = [customer for customer in customers.values() if customer["country_code"] == "NO"]
norwegian_orders = [order for customer in norwegian for order in orders_by_customer[customer["customer_id"]]]
# Decimal keeps each amount exact, so the total has no floating-point drift.
total = sum((Decimal(order["amount"]) for order in norwegian_orders), Decimal("0"))
print(f"Orders for NO customers: {len(norwegian_orders)}")
print(f"{norwegian[0]['name']}: {len(norwegian_orders)} orders, total {total:.2f}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";
import { parse } from "csv-parse/sync";

// The sample files are read from the folder named by TRAINING_DATA. Orders are joined to customers on customer_id.
const folder = process.env.TRAINING_DATA;
const customers = parse(readFileSync(path.join(folder, "customers.csv"), "utf8"), { columns: true });
const orders = parse(readFileSync(path.join(folder, "orders.csv"), "utf8"), { columns: true });
const ordersByCustomer = new Map();
for (const order of orders) {
  if (!ordersByCustomer.has(order.customer_id)) ordersByCustomer.set(order.customer_id, []);
  ordersByCustomer.get(order.customer_id).push(order);
}
const withoutOrders = customers.filter((customer) => !ordersByCustomer.has(customer.customer_id)).length;
console.log(`Customers: ${customers.length}`);
console.log(`Customers with no orders: ${withoutOrders}`);
const norwegian = customers.filter((customer) => customer.country_code === "NO");
const norwegianOrders = norwegian.flatMap((customer) => ordersByCustomer.get(customer.customer_id) ?? []);
// The amounts are summed in whole cents, so no binary float error builds up. The division happens once, at the end.
const cents = norwegianOrders.reduce((sum, order) => sum + Math.round(Number(order.amount) * 100), 0);
console.log(`Orders for NO customers: ${norwegianOrders.length}`);
console.log(`${norwegian[0].name}: ${norwegianOrders.length} orders, total ${(cents / 100).toFixed(2)}`);
```
~~~

The output is the same in every language:

~~~text
Customers: 12
Customers with no orders: 0
Orders for NO customers: 3
Lars Haugen: 3 orders, total 2575.50
~~~

Every customer is in the result, and none has zero orders. Lars Haugen's three orders are 980.00, 1520.40, and 75.10, and they total 2575.50. The count of customers is taken from the customer table, not the join, so a join that dropped customers would show a lower count in the orders report than in the customers report.

> **Aside: the left side decides the result.**
> In this sample the customers are the left side, and every customer stays, with or without orders. Swapping the sides would give a different answer to the same question, which is why each join states its left side.

> **Common mistake.** Building the join from the orders and expecting customers with no orders to appear. They don't. A customer with no orders is only visible when the join starts from the customers, as this sample does.

---
