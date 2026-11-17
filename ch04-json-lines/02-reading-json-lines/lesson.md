# Reading JSON Lines

Reading a JSON Lines file means a loop: read a line, parse it, use the record, and read the next line. The file is never held whole. The sample below does that for `customers.jsonl`, counts the records, and prints the first customer. It reads the file as a stream, which is the point of the format, so the same code works on a file much larger than this one.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// The sample file is read from the folder named by TRAINING_DATA, one line at a time. Each line is parsed as its own value.
using System.Text.Json;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers.jsonl");
var count = 0;
string firstId = null;
string firstName = null;
using var reader = new StreamReader(path, System.Text.Encoding.UTF8);
string line;
while ((line = reader.ReadLine()) != null)
{
    using var document = JsonDocument.Parse(line);
    var customer = document.RootElement;
    if (count == 0)
    {
        firstId = customer.GetProperty("customer_id").GetInt64().ToString();
        firstName = customer.GetProperty("name").GetString();
    }
    count++;
}
Console.WriteLine($"Records: {count}");
Console.WriteLine($"First customer: {firstId} {firstName}");
```
```python
import json
import os

# The sample file is read from the folder named by TRAINING_DATA, one line at a time. Each line is parsed as its own value.
path = os.path.join(os.environ["TRAINING_DATA"], "customers.jsonl")
count = 0
first = None
with open(path, encoding="utf-8") as handle:
    for line in handle:
        record = json.loads(line)
        if first is None:
            first = record
        count += 1
print(f"Records: {count}")
print(f"First customer: {first['customer_id']} {first['name']}")
```
```javascript
import { createReadStream } from "node:fs";
import path from "node:path";
import readline from "node:readline";

// The sample file is read from the folder named by TRAINING_DATA, one line at a time. Each line is parsed as its own value.
const input = createReadStream(path.join(process.env.TRAINING_DATA, "customers.jsonl"), { encoding: "utf8" });
const reader = readline.createInterface({ input, crlfDelay: Infinity });
let count = 0;
let first = null;
for await (const line of reader) {
  const record = JSON.parse(line);
  if (first === null) first = record;
  count++;
}
console.log(`Records: ${count}`);
console.log(`First customer: ${first.customer_id} ${first.name}`);
```
~~~

The output is the same in every language:

~~~text
Records: 12
First customer: 1001 Alice Carter
~~~

The three versions have the same shape. Each reads a line, parses it on its own, and keeps the count. The C# version disposes each parsed document inside the loop, so no document outlives its line. The JavaScript version uses `readline` with `crlfDelay` set to infinity, so a CRLF file is read the same as an LF file. The Python version relies on text mode, which strips the line ending for it.

Notice what the code does not do. It never builds a list of all the records, and it never waits for the end of the file before it starts counting. A program written this way uses the same memory for a file of twelve lines and a file of twelve million.

> **Aside: why `for await` in JavaScript?**
> The `readline` interface delivers lines over time, as the file is read, so the loop has to wait for each one. `for await` does that, and it works at the top level of a module, which is why this sample doesn't need a function around it.

> **Common mistake.** Reading the file with `readFileSync` and then splitting it on newlines. That works for this file, and it loads the whole file into memory first. For a file that matters, the stream is the right tool.

---
