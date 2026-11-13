# Reading YAML

Reading YAML means loading the text into the language's own values: a list of maps, in this file's case. Each library has a safe load call, and the sample uses it. The sample reads `customers.yaml`, counts the customers, and prints the first one. The balance is a quoted value, so each library keeps it as text, and the output shows the decimal places the file wrote.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package YamlDotNet@18.1.0

// The sample file is read from the folder named by TRAINING_DATA. The deserializer builds plain values, not arbitrary types.
using YamlDotNet.Serialization;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers.yaml");
var text = File.ReadAllText(path);
var deserializer = new DeserializerBuilder().Build();
var customers = deserializer.Deserialize<List<Dictionary<string, object>>>(text);
var first = customers[0];
var id = first["customer_id"];
var name = first["name"];
var balance = first["balance"];
Console.WriteLine($"Records: {customers.Count}");
Console.WriteLine($"First customer: {id} {name} {balance}");
```
```python
import os

import yaml

# The sample file is read from the folder named by TRAINING_DATA. safe_load builds plain values, not arbitrary types.
path = os.path.join(os.environ["TRAINING_DATA"], "customers.yaml")
with open(path, encoding="utf-8") as handle:
    customers = yaml.safe_load(handle)
first = customers[0]
print(f"Records: {len(customers)}")
print(f"First customer: {first['customer_id']} {first['name']} {first['balance']}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";
import { load } from "js-yaml";

// The sample file is read from the folder named by TRAINING_DATA. load builds plain values, and its default schema is safe.
const customers = load(readFileSync(path.join(process.env.TRAINING_DATA, "customers.yaml"), "utf8"));
const first = customers[0];
console.log(`Records: ${customers.length}`);
console.log(`First customer: ${first.customer_id} ${first.name} ${first.balance}`);
```
~~~

The output is the same in every language:

~~~text
Records: 12
First customer: 1001 Alice Carter 1250.75
~~~

The identifier, `1001`, is not quoted in the file, so each reader decides it's a number. The balance is quoted, so it stays text. The distinction is visible in the file and in the way each library returns values, and it's the reason the writer quoted the balance. If a program needs the balance as a number, it converts the text itself, as the money homework did.

The three calls are the same operation with different names. Each one reads the whole document and returns the list. The C# deserializer is given the type it should build, a list of dictionaries, which keeps the result to plain values. The Python and JavaScript loaders build plain values by default.

> **Aside: the safe loader is the default in the JavaScript sample.**
> `js-yaml` 5 uses the YAML 1.2 core schema when `load` is called without options, and that schema doesn't build language types. The Python call is `safe_load` for the same reason, and the C# sample uses a deserializer with no type tags registered.

> **Common mistake.** Calling a loader that builds arbitrary objects on a file from outside your system. Some YAML libraries offer a full loader that can create objects of named types. That loader executes behaviour the file requests, so use the safe loader on any untrusted input.

---
