# Nested Objects

Each customer in `customers.json` holds an `address` object, which holds three fields. A nested object is the natural shape for that data, and a program can use it directly. Two jobs come up often, though. A flat format such as CSV has no place for the nesting, so the object has to be flattened into dotted keys like `address.city`. And an API may want the nested part written back out as its own JSON.

The sample below does both for the first customer. It flattens the address into one line per field, then writes the address again as indented JSON. The output shows the nesting the writer keeps and the flattening the reader makes.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// The sample file is read from the folder named by TRAINING_DATA. The first customer's address is flattened, then written back as JSON.
using System.Text.Json;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers.json");
using var document = JsonDocument.Parse(File.ReadAllText(path, System.Text.Encoding.UTF8));
var first = document.RootElement[0];
var address = first.GetProperty("address");
foreach (var field in address.EnumerateObject())
{
    var value = field.Value.GetString();
    Console.WriteLine($"address.{field.Name} = {value}");
}
var options = new JsonSerializerOptions { WriteIndented = true };
Console.WriteLine(JsonSerializer.Serialize(address, options));
```
```python
import json
import os

# The sample file is read from the folder named by TRAINING_DATA. The first customer's address is flattened, then written back as JSON.
path = os.path.join(os.environ["TRAINING_DATA"], "customers.json")
with open(path, encoding="utf-8") as handle:
    customers = json.load(handle)
address = customers[0]["address"]
for field, value in address.items():
    print(f"address.{field} = {value}")
print(json.dumps(address, indent=2))
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";

// The sample file is read from the folder named by TRAINING_DATA. The first customer's address is flattened, then written back as JSON.
const customers = JSON.parse(readFileSync(path.join(process.env.TRAINING_DATA, "customers.json"), "utf8"));
const address = customers[0].address;
for (const [field, value] of Object.entries(address)) {
  console.log(`address.${field} = ${value}`);
}
console.log(JSON.stringify(address, null, 2));
```
~~~

The output is the same in every language:

~~~text
address.street = 12 Maple Street
address.city = Springfield
address.postal_code = 62704
{
  "street": "12 Maple Street",
  "city": "Springfield",
  "postal_code": "62704"
}
~~~

The flattened lines use a dot to show where each value sat in the nesting. A flat format can hold that name and value, but it can't hold the object itself, so nothing about `address` as a unit survives. The written JSON goes the other way: it keeps the three fields together under one key, which is what an API consumer would expect.

Notice that the postal code is written as a string, `"62704"`. It was a string in the file, because a postal code isn't a quantity, and leading zeros in some countries would be lost if it were a number. The type was chosen when the file was made, and the reader keeps it.

Flattening is a choice you make, and it can be lossy. A flattened key like `address.city` tells you nothing about whether `address` was optional or always present. The schema chapter returns to that.

> **Aside: the key order is kept.**
> The three fields come out in the order they were written, because all three parsers keep the order in the file. A flattening that sorts the keys would give a different output, and a reader comparing the two would see a difference that isn't in the data.

> **Common mistake.** Flattening by joining keys with a dot and calling it done, when the original key itself contains a dot. A key named `a.b` and a nested `a` with a key `b` both become `a.b`. Choose a separator that can't occur in a key, or check for collisions.

---
