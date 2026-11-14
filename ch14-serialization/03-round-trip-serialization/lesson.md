# Round-Trip Serialization

The reverse of the last sample is writing. The records are serialized from the program's types, written to a file, and read back, and the sample checks that each field came back as it went out. This is the round trip from Chapter 13, applied to a single mapping instead of a loop of formats.

The writing decisions are the same as the reading ones. C# writes the balance as a JSON number, because its decimal serializes that way. Python has no way to write a `Decimal` as a JSON number, so the sample writes it as a string and converts it back on the way in. JavaScript writes the number it holds. Each choice is valid, and each reads back to the same balance in value. The check compares values, not the text, because the text of a number can differ between writers, as the earlier chapters showed.

The sample uses the customers from `customers.json`, reads them, writes them, reads them again, and compares every field the records hold.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// The sample file is read from the folder named by TRAINING_DATA. The records are written, read back, and compared field by field.
using System.Text.Json;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers.json");
var original = JsonSerializer.Deserialize<List<Customer>>(File.ReadAllText(path, System.Text.Encoding.UTF8));
var written = JsonSerializer.Serialize(original, new JsonSerializerOptions { WriteIndented = true });
var back = JsonSerializer.Deserialize<List<Customer>>(written);
var matches = original.Count == back.Count && original.Zip(back).All(pair =>
    pair.First.customer_id == pair.Second.customer_id
    && pair.First.name == pair.Second.name
    && pair.First.balance == pair.Second.balance
    && pair.First.tags.SequenceEqual(pair.Second.tags));
Console.WriteLine($"Records written: {original.Count}");
Console.WriteLine($"Round trip matches: {(matches ? "yes" : "no")}");

class Customer
{
    public int customer_id { get; set; }
    public string name { get; set; } = "";
    public decimal balance { get; set; }
    public List<string> tags { get; set; } = new List<string>();
}
```
```python
import json
import os
from dataclasses import dataclass, field
from decimal import Decimal

# The sample file is read from the folder named by TRAINING_DATA. The records are written, read back, and compared field by field.
@dataclass
class Customer:
    customer_id: int
    name: str
    balance: Decimal
    tags: list = field(default_factory=list)


path = os.path.join(os.environ["TRAINING_DATA"], "customers.json")
with open(path, encoding="utf-8") as handle:
    original = [
        Customer(customer_id=record["customer_id"], name=record["name"], balance=Decimal(str(record["balance"])), tags=record["tags"])
        for record in json.load(handle, parse_float=Decimal)
    ]
# JSON has no decimal type, so each balance is written as a string and converted back on the way in.
written = json.dumps(
    [{"customer_id": c.customer_id, "name": c.name, "balance": str(c.balance), "tags": c.tags} for c in original],
    indent=2,
)
back = [
    Customer(customer_id=record["customer_id"], name=record["name"], balance=Decimal(record["balance"]), tags=record["tags"])
    for record in json.loads(written)
]
matches = len(original) == len(back) and all(
    a.customer_id == b.customer_id and a.name == b.name and a.balance == b.balance and a.tags == b.tags
    for a, b in zip(original, back)
)
print(f"Records written: {len(original)}")
print(f"Round trip matches: {'yes' if matches else 'no'}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";

// The sample file is read from the folder named by TRAINING_DATA. The records are written, read back, and compared field by field.
class Customer {
  constructor({ customer_id, name, balance, tags }) {
    this.customer_id = customer_id;
    this.name = name;
    this.balance = balance;
    this.tags = tags;
  }
}

const original = JSON.parse(readFileSync(path.join(process.env.TRAINING_DATA, "customers.json"), "utf8")).map((record) => new Customer(record));
const written = JSON.stringify(original, null, 2);
const back = JSON.parse(written).map((record) => new Customer(record));
const matches = original.length === back.length && original.every((customer, index) => {
  const other = back[index];
  return customer.customer_id === other.customer_id
    && customer.name === other.name
    && customer.balance === other.balance
    && JSON.stringify(customer.tags) === JSON.stringify(other.tags);
});
console.log(`Records written: ${original.length}`);
console.log(`Round trip matches: ${matches ? "yes" : "no"}`);
```
~~~

The output is the same in every language:

~~~text
Records written: 12
Round trip matches: yes
~~~

Every record came back with the same identifier, name, balance, and tags. The Python balance is written as text, so its JSON differs from the other two, but its value is the same. A round trip that compared the text of the two files would fail for that reason alone, and the test would be checking the writer, not the data.

> **Aside: write what you will read.**
> A writer that produces a format its own reader can't parse would fail the round trip at once. The round trip is most useful when it runs through the reader the rest of the pipeline uses, which is why these samples read back with the same mapping they wrote from.

> **Common mistake.** Writing a `Decimal` with the default JSON writer in Python. The writer raises an error, or the value is converted to a binary float on the way through. Choose the representation, and convert it on both sides.

---
