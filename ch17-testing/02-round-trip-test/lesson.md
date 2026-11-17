# Round-Trip Test

This test uses the first customer in `customers.json` as its fixture. The fixture is a real record from the sample data, so the expected values are the ones the earlier chapters checked by hand: the name `Alice Carter`, the balance `1250.75`, and the tags `vip` and `newsletter`. The test writes the record out with the language's JSON writer, reads it back, and checks each field against the fixture.

Each check prints a line with the word PASS or FAIL, and the label names the field, so a failure points at the field that changed. The totals at the end give the count of each. The checks are written so that a failure in one field does not hide the result for the others.

The round trip checks the serializer and the mapping together. A failure would show that a field changes when it is written and read again, which is the kind of change the serialization chapter was about.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// The fixture is the first customer in customers.json. It is written out, read back, and each field is checked.
using System.Text.Json;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers.json");
var fixture = JsonSerializer.Deserialize<List<Customer>>(File.ReadAllText(path, System.Text.Encoding.UTF8))[0];
var written = JsonSerializer.Serialize(fixture);
var back = JsonSerializer.Deserialize<Customer>(written);
var passed = 0;
var failed = 0;
void Check(string label, bool ok)
{
    Console.WriteLine($"{(ok ? "PASS" : "FAIL")}: {label}");
    if (ok) passed++; else failed++;
}
Check("name survives the round trip", back.name == fixture.name);
Check("balance survives the round trip", back.balance == fixture.balance);
Check("tags survive the round trip", back.tags.SequenceEqual(fixture.tags));
Console.WriteLine($"Checks passed: {passed}");
Console.WriteLine($"Checks failed: {failed}");

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

# The fixture is the first customer in customers.json. It is written out, read back, and each field is checked.
@dataclass
class Customer:
    customer_id: int
    name: str
    balance: Decimal
    tags: list = field(default_factory=list)


path = os.path.join(os.environ["TRAINING_DATA"], "customers.json")
with open(path, encoding="utf-8") as handle:
    first = json.load(handle, parse_float=Decimal)[0]
fixture = Customer(first["customer_id"], first["name"], first["balance"], first["tags"])
written = json.dumps({"customer_id": fixture.customer_id, "name": fixture.name, "balance": str(fixture.balance), "tags": fixture.tags})
loaded = json.loads(written)
back = Customer(loaded["customer_id"], loaded["name"], Decimal(loaded["balance"]), loaded["tags"])
passed = 0
failed = 0


def check(label, ok):
    global passed, failed
    print(f"{'PASS' if ok else 'FAIL'}: {label}")
    if ok:
        passed += 1
    else:
        failed += 1


check("name survives the round trip", back.name == fixture.name)
check("balance survives the round trip", back.balance == fixture.balance)
check("tags survive the round trip", back.tags == fixture.tags)
print(f"Checks passed: {passed}")
print(f"Checks failed: {failed}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";

// The fixture is the first customer in customers.json. It is written out, read back, and each field is checked.
const fixture = JSON.parse(readFileSync(path.join(process.env.TRAINING_DATA, "customers.json"), "utf8"))[0];
const written = JSON.stringify(fixture);
const back = JSON.parse(written);
let passed = 0;
let failed = 0;
function check(label, ok) {
  console.log(`${ok ? "PASS" : "FAIL"}: ${label}`);
  if (ok) passed++;
  else failed++;
}
check("name survives the round trip", back.name === fixture.name);
check("balance survives the round trip", back.balance === fixture.balance);
check("tags survive the round trip", JSON.stringify(back.tags) === JSON.stringify(fixture.tags));
console.log(`Checks passed: ${passed}`);
console.log(`Checks failed: ${failed}`);
```
~~~

The output is the same in every language:

~~~text
PASS: name survives the round trip
PASS: balance survives the round trip
PASS: tags survive the round trip
Checks passed: 3
Checks failed: 0
~~~

All three fields come back as they went out. The balance check is the one that matters most. It passes in C# and Python because each reads the balance as an exact decimal, and in JavaScript because `1250.75` is exact as a binary float. A balance such as `0.10` would fail the same check in JavaScript if it were written as a number, which the homework returns to.

> **Aside: the check is the claim the test makes.**
> Each `Check` line states one thing the program must keep. A reader who sees the label can tell what was tested without reading the code.

> **Common mistake.** Comparing the two records by their printed text. The text of a record can differ in the order of its keys or the spacing of its values, without any field having changed. Compare field by field.

---
