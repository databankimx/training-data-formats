# A Malformed Line

The file `orders-lines.jsonl` has twenty-four lines, one per order. The seventh line is damaged: its closing brace is missing, so it isn't valid JSON. The other twenty-three are fine.

This is where JSON Lines pays off. A JSON array with one damaged record can't be parsed at all, and the parser stops at the damage. With one record per line, the damage is confined. The sample below reads every line, counts the ones that parse, and records the number of each one that doesn't. The bad line is reported and then skipped, and the reading goes on to the end of the file.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// The sample file is read from the folder named by TRAINING_DATA. A line that won't parse is recorded and skipped.
using System.Text.Json;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "orders-lines.jsonl");
var lines = 0;
var parsed = 0;
var badLines = new List<int>();
using var reader = new StreamReader(path, System.Text.Encoding.UTF8);
string line;
while ((line = reader.ReadLine()) != null)
{
    lines++;
    try
    {
        using var document = JsonDocument.Parse(line);
        parsed++;
    }
    catch (JsonException)
    {
        badLines.Add(lines);
    }
}
var badText = string.Join(", ", badLines);
Console.WriteLine($"Lines read: {lines}");
Console.WriteLine($"Parsed: {parsed}");
Console.WriteLine($"Could not parse: line {badText}");
```
```python
import json
import os

# The sample file is read from the folder named by TRAINING_DATA. A line that won't parse is recorded and skipped.
path = os.path.join(os.environ["TRAINING_DATA"], "orders-lines.jsonl")
lines = 0
parsed = 0
bad_lines = []
with open(path, encoding="utf-8") as handle:
    for number, line in enumerate(handle, start=1):
        lines += 1
        try:
            json.loads(line)
            parsed += 1
        except json.JSONDecodeError:
            bad_lines.append(number)
print(f"Lines read: {lines}")
print(f"Parsed: {parsed}")
print(f"Could not parse: line {', '.join(str(number) for number in bad_lines)}")
```
```javascript
import { createReadStream } from "node:fs";
import path from "node:path";
import readline from "node:readline";

// The sample file is read from the folder named by TRAINING_DATA. A line that won't parse is recorded and skipped.
const input = createReadStream(path.join(process.env.TRAINING_DATA, "orders-lines.jsonl"), { encoding: "utf8" });
const reader = readline.createInterface({ input, crlfDelay: Infinity });
let lines = 0;
let parsed = 0;
const badLines = [];
for await (const line of reader) {
  lines++;
  try {
    JSON.parse(line);
    parsed++;
  } catch (error) {
    badLines.push(lines);
  }
}
console.log(`Lines read: ${lines}`);
console.log(`Parsed: ${parsed}`);
console.log(`Could not parse: line ${badLines.join(", ")}`);
```
~~~

The output is the same in every language:

~~~text
Lines read: 24
Parsed: 23
Could not parse: line 7
~~~

The count of lines read is twenty-four, and the count parsed is twenty-three. The one that failed is line seven, and that is the number the program reports, so someone can find it in the file. The program didn't stop there. Lines eight to twenty-four, seventeen in all, were read and parsed after it.

Each language catches its own error type, and the sample catches only that type. C# catches `JsonException`, Python catches `json.JSONDecodeError`, and JavaScript catches the `SyntaxError` that `JSON.parse` throws. An error that isn't a parse error, such as a file that can't be opened, still stops the program, which is what should happen.

> **Aside: line numbers count from one.**
> Editors show line one at the top, so the report uses the same numbering. A program that counted from zero would send the reader to the wrong line.

> **Common mistake.** Reporting the damage and then discarding the whole file. A pipeline that does that loses the twenty-three good records along with the one bad one. Keep the good records, and route the bad line to a list where it can be fixed.

---
