# JSON to JSON Lines

This link reads `customers.json` from the chain folder and writes `customers.jsonl`, one compact object per line. The records are the same, and so is the shape of each one. The only change is the layout: a JSON array becomes a sequence of lines, with no brackets and no commas between records.

The writer writes each record on its own, so a record can be checked, appended, or read without the others. That's the property Chapter 4 covered, and the next links depend on it only through the file's content, not its layout.

The output is the number of records written.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// The array is read from the chain folder, and each element is written as one compact line for the next link to read.
using System.Text.Json;
var source = Path.Combine(Environment.GetEnvironmentVariable("CHAIN_DATA"), "customers.json");
var target = Path.Combine(Environment.GetEnvironmentVariable("CHAIN_DATA"), "customers.jsonl");
using var document = JsonDocument.Parse(File.ReadAllText(source, System.Text.Encoding.UTF8));
var lines = document.RootElement.EnumerateArray().Select(record => JsonSerializer.Serialize(record)).ToList();
File.WriteAllLines(target, lines, new System.Text.UTF8Encoding(false));
Console.WriteLine($"Records written: {lines.Count}");
```
```python
import json
import os

# The array is read from the chain folder, and each element is written as one compact line for the next link to read.
source = os.path.join(os.environ["CHAIN_DATA"], "customers.json")
target = os.path.join(os.environ["CHAIN_DATA"], "customers.jsonl")
with open(source, encoding="utf-8") as handle:
    records = json.load(handle)
with open(target, "w", encoding="utf-8", newline="\n") as handle:
    for record in records:
        handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
print(f"Records written: {len(records)}")
```
```javascript
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";

// The array is read from the chain folder, and each element is written as one compact line for the next link to read.
const records = JSON.parse(readFileSync(path.join(process.env.CHAIN_DATA, "customers.json"), "utf8"));
writeFileSync(path.join(process.env.CHAIN_DATA, "customers.jsonl"), records.map((record) => JSON.stringify(record)).join("\n") + "\n", "utf8");
console.log(`Records written: ${records.length}`);
```
~~~

The output is the same in every language:

~~~text
Records written: 12
~~~

The C# writer serializes each record again in compact form. It must not use the record's raw text: that text keeps the line breaks and indentation of the array it was read from, so a record would span several lines and the next link would fail to parse it. The Python and JavaScript writers serialize each record compactly for the same reason, and the values are identical in every language.

> **Aside: a line is the unit of a JSON Lines file.**
> Each line must be a complete value with no newline inside it. The compact form has no line breaks, which is why the writers use it.

> **Common mistake.** Taking the raw text of a value from a pretty-printed file. Its line breaks and indentation come with it, and a line-based format needs a single line. Serialize the value again in compact form.

---
