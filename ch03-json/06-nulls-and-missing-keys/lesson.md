# Nulls and Missing Keys

The file `customers-null-mix.json` has three records, and each shows a different way of having no value. The first has an `email` that is `null`. The second has `tags` that is `null`. The third has no `email` key at all. The records are short on purpose, so the three cases are easy to see.

A null says the field is there and holds nothing. A missing key says nothing about the field. For a program, that difference can matter. An API might mean "clear this value" when it sends a null, and "leave it unchanged" when it omits the key. A form might mean "no answer" for a null and "not asked" for a missing key. Treating them the same loses that meaning.

The sample below prints the status of `email` and `tags` for each record. The status is one of `missing`, `null`, or `present`. Each language has its own way of asking whether a key exists, and the sample uses it.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// The sample file is read from the folder named by TRAINING_DATA. A key is missing, null, or present, and the sample reports which.
using System.Text.Json;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers-null-mix.json");
using var document = JsonDocument.Parse(File.ReadAllText(path, System.Text.Encoding.UTF8));
foreach (var record in document.RootElement.EnumerateArray())
{
    var id = record.GetProperty("customer_id").GetInt64();
    var email = Status(record, "email");
    var tags = Status(record, "tags");
    Console.WriteLine($"{id}: email {email}, tags {tags}");
}

// Reports whether a key is missing, holds null, or holds a value.
string Status(JsonElement record, string key)
{
    if (!record.TryGetProperty(key, out var value)) return "missing";
    return value.ValueKind == JsonValueKind.Null ? "null" : "present";
}
```
```python
import json
import os

# The sample file is read from the folder named by TRAINING_DATA. A key is missing, null, or present, and the sample reports which.
path = os.path.join(os.environ["TRAINING_DATA"], "customers-null-mix.json")
with open(path, encoding="utf-8") as handle:
    records = json.load(handle)


def status(record, key):
    # "in" tells a missing key from a null value. A plain record.get would give None for both.
    if key not in record:
        return "missing"
    return "null" if record[key] is None else "present"


for record in records:
    print(f"{record['customer_id']}: email {status(record, 'email')}, tags {status(record, 'tags')}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";

// The sample file is read from the folder named by TRAINING_DATA. A key is missing, null, or present, and the sample reports which.
const records = JSON.parse(readFileSync(path.join(process.env.TRAINING_DATA, "customers-null-mix.json"), "utf8"));

// "in" tells a missing key from a null value. A plain record.key lookup gives undefined for a missing key and null for a null one.
function status(record, key) {
  if (!(key in record)) return "missing";
  return record[key] === null ? "null" : "present";
}

for (const record of records) {
  console.log(`${record.customer_id}: email ${status(record, "email")}, tags ${status(record, "tags")}`);
}
```
~~~

The output is the same in every language:

~~~text
1001: email null, tags present
1002: email present, tags null
1003: email missing, tags present
~~~

Read the first line. The first customer's `email` is `null`, so the key is there and holds nothing. Its `tags` is an empty list, which is a value, so the status is `present`. An empty list and a null are different things, and the sample keeps them apart. The third customer's `email` is missing entirely, and the status says so.

The Python and JavaScript samples both have a comment about a plain lookup. In Python, `record.get("email")` returns `None` for a missing key, the same as a null. In JavaScript, a missing key gives `undefined`, and a null gives `null`, which is different, but a check like `if (!record.email)` treats both as absent, and so does an empty string. The `in` operator in Python and JavaScript, and `TryGetProperty` in C#, ask about the key itself.

> **Aside: the empty string is a third case.**
> A value of `""` is present and holds an empty string. It's neither null nor missing. Checking `if (name)` in JavaScript, or `if name:` in Python, treats it as absent too. The schema chapter depends on telling these apart.

> **Common mistake.** Writing `if (record.email)` to test for a value. It's false for a null, a missing key, an empty string, and a zero. The test answers a different question from the one you meant to ask.

---
