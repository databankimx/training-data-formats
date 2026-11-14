# Parquet to CSV

This is the last link, and it closes the loop. It reads `customers.parquet` from the chain folder, writes `customers-chain.csv`, and then compares that file with the original `customers.csv` from the sample data. The comparison is the test of the whole chain, and it reports two results.

The first is whether the balances are equal as numbers. The second is whether every row is equal as text. The two can differ. A balance of `0.00` and a balance of `0` are equal in value and different in text, and that's exactly the loss the Excel link introduced. This link writes each balance with two decimal places, which restores the text, so both results should say yes. If the text check fails, the chain has lost something that the value check cannot see.

The output is three lines: the number of rows compared, and the two results.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package CsvHelper@33.1.0
#:package Parquet.Net@5.6.1

// The Parquet is read from the chain folder, written back to CSV there, and compared with the original customers.csv.
using System.Globalization;
using CsvHelper;
using CsvHelper.Configuration;
using Parquet.Serialization;
var chain = Environment.GetEnvironmentVariable("CHAIN_DATA");
var original = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers.csv");
var written = Path.Combine(chain, "customers-chain.csv");
var customers = await ParquetSerializer.DeserializeAsync<FlatCustomer>(Path.Combine(chain, "customers.parquet"));
var header = "customer_id,name,email,signup_date,balance,active,country_code,address_street,address_city,address_postal_code,tags";
var lines = new List<string> { header };
foreach (var customer in customers)
{
    var fields = new[]
    {
        customer.customer_id.ToString(CultureInfo.InvariantCulture), customer.name, customer.email, customer.signup_date,
        customer.balance.ToString("F2", CultureInfo.InvariantCulture), customer.active ? "true" : "false", customer.country_code,
        customer.address_street, customer.address_city, customer.address_postal_code, customer.tags,
    };
    lines.Add(string.Join(",", fields.Select(field => field.Contains(',') ? "\"" + field + "\"" : field)));
}
File.WriteAllLines(written, lines, new System.Text.UTF8Encoding(false));
var expected = ReadRows(original);
var actual = ReadRows(written);
var valuesEqual = expected.Count == actual.Count && expected.Zip(actual).All(pair => pair.First.Length == pair.Second.Length && pair.First.Zip(pair.Second).All(field => field.First == field.Second || (decimal.TryParse(field.First, NumberStyles.Number, CultureInfo.InvariantCulture, out var a) && decimal.TryParse(field.Second, NumberStyles.Number, CultureInfo.InvariantCulture, out var b) && a == b)));
var textEqual = expected.Count == actual.Count && expected.Zip(actual).All(pair => pair.First.SequenceEqual(pair.Second));
Console.WriteLine($"Rows compared: {expected.Count - 1}");
Console.WriteLine($"Balances equal in value: {(valuesEqual ? "yes" : "no")}");
Console.WriteLine($"Rows equal in text: {(textEqual ? "yes" : "no")}");

// Reads every row of a CSV file, header included, into arrays of fields.
List<string[]> ReadRows(string file)
{
    var rows = new List<string[]>();
    using var reader = new CsvReader(new StreamReader(file, System.Text.Encoding.UTF8), new CsvConfiguration(CultureInfo.InvariantCulture));
    while (reader.Read())
    {
        rows.Add(reader.Parser.Record);
    }
    return rows;
}

class FlatCustomer
{
    public long customer_id { get; set; }
    public string name { get; set; } = "";
    public string email { get; set; } = "";
    public string signup_date { get; set; } = "";
    public decimal balance { get; set; }
    public bool active { get; set; }
    public string country_code { get; set; } = "";
    public string address_street { get; set; } = "";
    public string address_city { get; set; } = "";
    public string address_postal_code { get; set; } = "";
    public string tags { get; set; } = "";
}
```
```python
import csv
import os
from decimal import Decimal

import pyarrow.parquet as pq

# The Parquet is read from the chain folder, written back to CSV there, and compared with the original customers.csv.
chain = os.environ["CHAIN_DATA"]
original = os.path.join(os.environ["TRAINING_DATA"], "customers.csv")
written = os.path.join(chain, "customers-chain.csv")
header = ["customer_id", "name", "email", "signup_date", "balance", "active", "country_code", "address_street", "address_city", "address_postal_code", "tags"]
rows = pq.read_table(os.path.join(chain, "customers.parquet")).to_pylist()
with open(written, "w", encoding="utf-8", newline="") as handle:
    writer = csv.writer(handle, lineterminator="\n")
    writer.writerow(header)
    for row in rows:
        writer.writerow([
            str(row["customer_id"]), row["name"], row["email"], row["signup_date"],
            f"{row['balance']:.2f}", "true" if row["active"] else "false", row["country_code"],
            row["address_street"], row["address_city"], row["address_postal_code"], row["tags"],
        ])


def read_rows(file):
    with open(file, encoding="utf-8", newline="") as handle:
        return list(csv.reader(handle))


expected = read_rows(original)
actual = read_rows(written)


def same_value(first, second):
    if first == second:
        return True
    try:
        return Decimal(first) == Decimal(second)
    except ArithmeticError:
        return False


values_equal = len(expected) == len(actual) and all(
    len(a) == len(b) and all(same_value(x, y) for x, y in zip(a, b)) for a, b in zip(expected, actual)
)
text_equal = expected == actual
print(f"Rows compared: {len(expected) - 1}")
print(f"Balances equal in value: {'yes' if values_equal else 'no'}")
print(f"Rows equal in text: {'yes' if text_equal else 'no'}")
```
```javascript
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { asyncBufferFromFile, parquetReadObjects } from "hyparquet";
import { parse } from "csv-parse/sync";
import { stringify } from "csv-stringify/sync";

// The Parquet is read from the chain folder, written back to CSV there, and compared with the original customers.csv.
const chain = process.env.CHAIN_DATA;
const original = path.join(process.env.TRAINING_DATA, "customers.csv");
const written = path.join(chain, "customers-chain.csv");
const header = ["customer_id", "name", "email", "signup_date", "balance", "active", "country_code", "address_street", "address_city", "address_postal_code", "tags"];
const customers = await parquetReadObjects({ file: await asyncBufferFromFile(path.join(chain, "customers.parquet")) });
const rows = customers.map((row) => [
  String(row.customer_id), row.name, row.email, row.signup_date,
  Number(row.balance).toFixed(2), row.active ? "true" : "false", row.country_code,
  row.address_street, row.address_city, row.address_postal_code, row.tags,
]);
writeFileSync(written, stringify([header, ...rows]), "utf8");

const expected = parse(readFileSync(original, "utf8"));
const actual = parse(readFileSync(written, "utf8"));
const same = (first, second) => first === second || (!Number.isNaN(Number(first)) && !Number.isNaN(Number(second)) && Number(first) === Number(second));
const valuesEqual = expected.length === actual.length && expected.every((row, index) =>
  row.length === actual[index].length && row.every((field, column) => same(field, actual[index][column])));
const textEqual = JSON.stringify(expected) === JSON.stringify(actual);
console.log(`Rows compared: ${expected.length - 1}`);
console.log(`Balances equal in value: ${valuesEqual ? "yes" : "no"}`);
console.log(`Rows equal in text: ${textEqual ? "yes" : "no"}`);
```
~~~

The output is the same in every language:

~~~text
Rows compared: 12
Balances equal in value: yes
Rows equal in text: yes
~~~

The loop is closed. Each link read the output of the one before it, and the last file matches the original on values and on text. The text check passes only because this link formats the balance to two places. A version of the chain that wrote the balance as a bare number would pass the value check and fail the text check, and the lesson's point is that a test of values alone would have hidden that.

> **Aside: a loop tests every link at once.**
> A round trip tests one format. A loop tests the whole sequence, so a loss in the fifth link can show up only in the ninth. The check at the end is the only place it can be seen.

> **Common mistake.** Comparing the two files as bytes. The line endings and the quoting differ between writers, so the bytes fail even when every value matches. Compare the parsed fields, as these samples do.

---
