# Reading JSON

`customers.json` is a single array with twelve objects, one per customer. Reading it takes three steps in every language: read the file as text, parse the text, then use the result. The parser turns the array into the language's own list, and each object into its own map, dictionary, or object.

The sample below reads the file, counts the records, and prints the identifier and name of the first one. It is the same job in each language, and the output is the same.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// The sample file is read from the folder named by TRAINING_DATA. The parser reads the whole array.
using System.Text.Json;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers.json");
using var document = JsonDocument.Parse(File.ReadAllText(path, System.Text.Encoding.UTF8));
var customers = document.RootElement;
Console.WriteLine($"Records: {customers.GetArrayLength()}");
var first = customers[0];
var firstId = first.GetProperty("customer_id").GetInt64();
var firstName = first.GetProperty("name").GetString();
Console.WriteLine($"First customer: {firstId} {firstName}");
```
```python
import json
import os

# The sample file is read from the folder named by TRAINING_DATA. The parser reads the whole array.
path = os.path.join(os.environ["TRAINING_DATA"], "customers.json")
with open(path, encoding="utf-8") as handle:
    customers = json.load(handle)
print(f"Records: {len(customers)}")
first = customers[0]
print(f"First customer: {first['customer_id']} {first['name']}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";

// The sample file is read from the folder named by TRAINING_DATA. The parser reads the whole array.
const customers = JSON.parse(readFileSync(path.join(process.env.TRAINING_DATA, "customers.json"), "utf8"));
console.log(`Records: ${customers.length}`);
const first = customers[0];
console.log(`First customer: ${first.customer_id} ${first.name}`);
```
~~~

The output is the same in every language:

~~~text
Records: 12
First customer: 1001 Alice Carter
~~~

Look at how each language reaches the identifier. Python and JavaScript index the object directly, with `first['customer_id']` and `first.customer_id`. C# asks the element for a property and then for its type, with `GetProperty` and `GetInt64`. The C# version is more verbose, because the parser doesn't guess at types. It hands you the value as the kind of JSON it is, and you say which type you want. That verbosity is also the reason the large-integer sample is in C# with a different type.

The file is read as UTF-8, and the name `Alice Carter` is plain ASCII, so the output is the same in every console.

> **Aside: the parser reads the whole file.**
> Each of these calls parses the entire array before it returns. A file this size is fine, but a multi-gigabyte array would need a streaming reader. This tutorial doesn't cover streaming, so look for it in the libraries' own documentation when a file gets that large.

> **Common mistake.** Reading the file with a text reader and splitting it on commas or braces. JSON allows commas and braces inside strings, so a split breaks on valid data. Parse the file.

---
