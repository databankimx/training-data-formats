# TSV to JSON

This link reads `customers.tsv`, which the previous link wrote into the chain folder, and writes `customers.json` back into the chain folder. The JSON has the shape used in the earlier CSV-to-JSON work: the tags become a list, the three address columns become a nested object, the `active` text becomes a boolean, and the balance stays as text.

Keeping the balance as text is a deliberate choice, and the chain depends on it. A JSON number would be read back by some parsers as a binary float, which can't hold `1250.75` exactly. The text keeps the value exactly as written, and the later links decide how to store it. The postal code also stays text, so its leading zeros survive.

The output is the number of records written, and the JSON file is the input to the next link.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package CsvHelper@33.1.0

// The TSV is read from the chain folder, and the JSON is written there for the next link to read.
using System.Globalization;
using System.Text.Json;
using CsvHelper;
using CsvHelper.Configuration;
var source = Path.Combine(Environment.GetEnvironmentVariable("CHAIN_DATA"), "customers.tsv");
var target = Path.Combine(Environment.GetEnvironmentVariable("CHAIN_DATA"), "customers.json");
var rows = new List<string[]>();
using (var reader = new CsvReader(new StreamReader(source, System.Text.Encoding.UTF8), new CsvConfiguration(CultureInfo.InvariantCulture) { Delimiter = "\t" }))
{
    while (reader.Read())
    {
        rows.Add(reader.Parser.Record);
    }
}
var header = rows[0];
string Value(string[] row, string column) => row[Array.IndexOf(header, column)];
var records = rows.Skip(1).Select(row => new
{
    customer_id = int.Parse(Value(row, "customer_id")),
    name = Value(row, "name"),
    email = Value(row, "email"),
    signup_date = Value(row, "signup_date"),
    balance = Value(row, "balance"),
    active = Value(row, "active") == "true",
    country_code = Value(row, "country_code"),
    address = new
    {
        street = Value(row, "address_street"),
        city = Value(row, "address_city"),
        postal_code = Value(row, "address_postal_code"),
    },
    tags = Value(row, "tags").Split(';', StringSplitOptions.RemoveEmptyEntries),
}).ToList();
File.WriteAllText(target, JsonSerializer.Serialize(records, new JsonSerializerOptions { WriteIndented = true }));
Console.WriteLine($"Records written: {records.Count}");
```
```python
import csv
import json
import os

# The TSV is read from the chain folder, and the JSON is written there for the next link to read.
source = os.path.join(os.environ["CHAIN_DATA"], "customers.tsv")
target = os.path.join(os.environ["CHAIN_DATA"], "customers.json")
with open(source, encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle, delimiter="\t"))
records = [
    {
        "customer_id": int(row["customer_id"]),
        "name": row["name"],
        "email": row["email"],
        "signup_date": row["signup_date"],
        "balance": row["balance"],
        "active": row["active"] == "true",
        "country_code": row["country_code"],
        "address": {
            "street": row["address_street"],
            "city": row["address_city"],
            "postal_code": row["address_postal_code"],
        },
        "tags": [tag for tag in row["tags"].split(";") if tag],
    }
    for row in rows
]
with open(target, "w", encoding="utf-8") as handle:
    json.dump(records, handle, indent=2, ensure_ascii=False)
print(f"Records written: {len(records)}")
```
```javascript
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { parse } from "csv-parse/sync";

// The TSV is read from the chain folder, and the JSON is written there for the next link to read.
const rows = parse(readFileSync(path.join(process.env.CHAIN_DATA, "customers.tsv"), "utf8"), { columns: true, delimiter: "\t" });
const records = rows.map((row) => ({
  customer_id: Number(row.customer_id),
  name: row.name,
  email: row.email,
  signup_date: row.signup_date,
  balance: row.balance,
  active: row.active === "true",
  country_code: row.country_code,
  address: {
    street: row.address_street,
    city: row.address_city,
    postal_code: row.address_postal_code,
  },
  tags: row.tags.split(";").filter((tag) => tag !== ""),
}));
writeFileSync(path.join(process.env.CHAIN_DATA, "customers.json"), JSON.stringify(records, null, 2), "utf8");
console.log(`Records written: ${records.length}`);
```
~~~

The output is the same in every language:

~~~text
Records written: 12
~~~

The JSON uses two-space indentation in every language, so the file looks the same to a reader and to a comparison of the text. The key order follows the order of the fields in the code, which is the order of the TSV columns. One difference is in the text of the file, not its values: the C# writer escapes accented letters such as `é` as `\u00E9`, while the Python and JavaScript writers keep them as they are. Parsed back, the values are identical, and the chain's final check compares values, so the difference does not break it.

> **Aside: the chain's JSON is the hub.**
> Every later link reads or writes this shape, so a mistake here, such as a balance that becomes a number, would be carried through the whole loop. The check at the end of the chain exists to catch that kind of mistake.

> **Common mistake.** Writing a JSON number for the balance because it looks like a number. The next links would then read a float, and the first decimal of a balance such as `0.10` would be inexact. Keep the balance as text here.

---
