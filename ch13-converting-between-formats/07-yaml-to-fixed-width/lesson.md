# YAML to Fixed-Width

This link reads `customers.yaml` and writes `customers.fixed`. The layout is an extension of the one from Chapter 6. The first six fields are the same, and five more are added after the country code: the street, the city, the postal code, the tags, and the email. Without the extra fields, the address and the tags would be lost here, and the chain would fail its final check for a reason that has nothing to do with the data.

| Field | Start | Width | Alignment |
|---|---|---|---|
| customer_id | 1 | 6 | right |
| name | 8 | 20 | left |
| signup_date | 29 | 10 | left |
| balance | 40 | 8 | right |
| active | 49 | 5 | left |
| country_code | 55 | 2 | left |
| address_street | 58 | 26 | left |
| address_city | 85 | 20 | left |
| address_postal_code | 106 | 10 | left |
| tags | 117 | 30 | left |
| email | 148 | 32 | left |

Each field is padded to its width, and a single space separates one field from the next, so every field starts at the position in the table. A value wider than its column is refused. A writer that truncated it would produce a line that reads back with a different value, and the error would show up only at the final check, far from its cause.

The fixed-width layout counts characters, not bytes. The file is written as UTF-8, so a name such as `Renée Dubois` has a fixed width in characters, and the next link reads it back by characters. Chapter 6 showed what happens when a reader counts bytes instead.

The output is the number of records written.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package YamlDotNet@18.1.0

// The YAML is read from the chain folder, and each customer is written as one fixed-width line for the next link to read.
using System.Globalization;
using YamlDotNet.Serialization;
var source = Path.Combine(Environment.GetEnvironmentVariable("CHAIN_DATA"), "customers.yaml");
var target = Path.Combine(Environment.GetEnvironmentVariable("CHAIN_DATA"), "customers.fixed");
var customers = new DeserializerBuilder().Build().Deserialize<List<Customer>>(File.ReadAllText(source, System.Text.Encoding.UTF8));
// Inline data, not from a sample file. The layout: each field's width, and whether it is right-aligned.
var widths = new[] { 6, 20, 10, 8, 5, 2, 26, 20, 10, 30, 32 };
var rightAligned = new[] { true, false, false, true, false, false, false, false, false, false, false };
var lines = new List<string>();
foreach (var customer in customers)
{
    var values = new[]
    {
        customer.customer_id.ToString(CultureInfo.InvariantCulture), customer.name, customer.signup_date,
        customer.balance, customer.active ? "true" : "false", customer.country_code,
        customer.address.street, customer.address.city, customer.address.postal_code,
        string.Join(";", customer.tags), customer.email,
    };
    var fields = new List<string>();
    for (var index = 0; index < values.Length; index++)
    {
        if (values[index].Length > widths[index])
        {
            throw new InvalidOperationException($"Customer {customer.customer_id}: a value is wider than its column ({widths[index]})");
        }
        fields.Add(rightAligned[index] ? values[index].PadLeft(widths[index]) : values[index].PadRight(widths[index]));
    }
    lines.Add(string.Join(" ", fields));
}
File.WriteAllLines(target, lines, new System.Text.UTF8Encoding(false));
Console.WriteLine($"Records written: {lines.Count}");

class Customer
{
    public int customer_id { get; set; }
    public string name { get; set; } = "";
    public string email { get; set; } = "";
    public string signup_date { get; set; } = "";
    public string balance { get; set; } = "";
    public bool active { get; set; }
    public string country_code { get; set; } = "";
    public Address address { get; set; } = new Address();
    public List<string> tags { get; set; } = new List<string>();
}

class Address
{
    public string street { get; set; } = "";
    public string city { get; set; } = "";
    public string postal_code { get; set; } = "";
}
```
```python
import os

import yaml

# The YAML is read from the chain folder, and each customer is written as one fixed-width line for the next link to read.
source = os.path.join(os.environ["CHAIN_DATA"], "customers.yaml")
target = os.path.join(os.environ["CHAIN_DATA"], "customers.fixed")
with open(source, encoding="utf-8") as handle:
    customers = yaml.safe_load(handle)
# Inline data, not from a sample file. The layout: each field's width, and whether it is right-aligned.
widths = [6, 20, 10, 8, 5, 2, 26, 20, 10, 30, 32]
right_aligned = [True, False, False, True, False, False, False, False, False, False, False]
lines = []
for customer in customers:
    balance = customer["balance"]
    # A balance that the YAML writer left as a bare number is written with two places, so it reads back as text.
    if not isinstance(balance, str):
        balance = f"{balance:.2f}"
    values = [
        str(customer["customer_id"]), customer["name"], customer["signup_date"],
        balance, "true" if customer["active"] else "false", customer["country_code"],
        customer["address"]["street"], customer["address"]["city"], customer["address"]["postal_code"],
        ";".join(customer["tags"]), customer["email"],
    ]
    fields = []
    for index, value in enumerate(values):
        if len(value) > widths[index]:
            raise ValueError(f"Customer {customer['customer_id']}: a value is wider than its column ({widths[index]})")
        fields.append(value.rjust(widths[index]) if right_aligned[index] else value.ljust(widths[index]))
    lines.append(" ".join(fields))
with open(target, "w", encoding="utf-8", newline="\n") as handle:
    handle.write("\n".join(lines) + "\n")
print(f"Records written: {len(lines)}")
```
```javascript
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { load } from "js-yaml";

// The YAML is read from the chain folder, and each customer is written as one fixed-width line for the next link to read.
const customers = load(readFileSync(path.join(process.env.CHAIN_DATA, "customers.yaml"), "utf8"));
// Inline data, not from a sample file. The layout: each field's width, and whether it is right-aligned.
const widths = [6, 20, 10, 8, 5, 2, 26, 20, 10, 30, 32];
const rightAligned = [true, false, false, true, false, false, false, false, false, false, false];
const lines = customers.map((customer) => {
  // A balance that the YAML writer left as a bare number is written with two places, so it reads back as text.
  const balance = typeof customer.balance === "string" ? customer.balance : Number(customer.balance).toFixed(2);
  const values = [
    String(customer.customer_id), customer.name, customer.signup_date,
    balance, customer.active ? "true" : "false", customer.country_code,
    customer.address.street, customer.address.city, customer.address.postal_code,
    customer.tags.join(";"), customer.email,
  ];
  const fields = values.map((value, index) => {
    if (value.length > widths[index]) {
      throw new Error(`Customer ${customer.customer_id}: a value is wider than its column (${widths[index]})`);
    }
    return rightAligned[index] ? value.padStart(widths[index]) : value.padEnd(widths[index]);
  });
  return fields.join(" ");
});
writeFileSync(path.join(process.env.CHAIN_DATA, "customers.fixed"), lines.join("\n") + "\n", "utf8");
console.log(`Records written: ${lines.length}`);
```
~~~

The output is the same in every language:

~~~text
Records written: 12
~~~

Every line is 179 characters long, and the balance ends at position 47, the same as Chapter 6. The fields are padded by character count, which the next link relies on. A balance that a YAML writer left as a bare number is written with two decimal places, so `0` becomes `0.00`, and the text matches the original.

> **Aside: the layout is the schema of this format.**
> Fixed-width has no names in the file. The layout is the only description of the columns, so it has to be written down and kept with the file, as the last step of Chapter 6 said.

> **Common mistake.** Letting a wide value silently run into the next column. The padding functions pass a long value through unchanged, and every field after it moves. Check each width before writing, as these samples do.

---
