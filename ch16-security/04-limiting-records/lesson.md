# Limiting Records

A streamed file can be much larger than any single record, and a feed can be endless. A program that reads it to the end without a limit spends its time and memory on input nobody asked it to process. The defence is a limit on how many records are read, and a program that reaches the limit stops reading and says so.

This sample reads `orders-lines.jsonl` as a stream, and it stops after ten lines. The file has twenty-four lines, so the limit is reached, and the remaining fourteen are never parsed. The file also has the malformed line from the JSON Lines chapter, on line seven, which is one of the ten lines read. The report therefore shows ten lines read, nine records parsed, and a stop at the limit.

The limit counts lines, not records, so a malformed line uses up the limit as well as a good one. A limit on parsed records would let an input of nothing but malformed lines run forever, which is the case the limit exists to stop.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// The sample file is read as a stream, and reading stops at the limit. Lines past the limit are never parsed.
using System.Text.Json;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "orders-lines.jsonl");
// Inline data, not from a sample file. The number of lines the program is willing to read.
const int limit = 10;
var read = 0;
var parsed = 0;
var stopped = false;
foreach (var line in File.ReadLines(path, System.Text.Encoding.UTF8))
{
    if (read == limit)
    {
        stopped = true;
        break;
    }
    read++;
    try
    {
        using var document = JsonDocument.Parse(line);
        parsed++;
    }
    catch (JsonException)
    {
        // A line that does not parse is counted as read, and it uses up the limit.
    }
}
Console.WriteLine($"Lines read: {read}");
Console.WriteLine($"Records parsed: {parsed}");
Console.WriteLine($"Stopped at the limit: {(stopped ? "yes" : "no")}");
```
```python
import json
import os

# The sample file is read as a stream, and reading stops at the limit. Lines past the limit are never parsed.
path = os.path.join(os.environ["TRAINING_DATA"], "orders-lines.jsonl")
# Inline data, not from a sample file. The number of lines the program is willing to read.
limit = 10
read = 0
parsed = 0
stopped = False
with open(path, encoding="utf-8") as handle:
    for line in handle:
        if read == limit:
            stopped = True
            break
        read += 1
        try:
            json.loads(line)
            parsed += 1
        except json.JSONDecodeError:
            # A line that does not parse is counted as read, and it uses up the limit.
            pass
print(f"Lines read: {read}")
print(f"Records parsed: {parsed}")
print(f"Stopped at the limit: {'yes' if stopped else 'no'}")
```
```javascript
import { createReadStream } from "node:fs";
import path from "node:path";
import readline from "node:readline";

// The sample file is read as a stream, and reading stops at the limit. Lines past the limit are never parsed.
const reader = readline.createInterface({
  input: createReadStream(path.join(process.env.TRAINING_DATA, "orders-lines.jsonl"), { encoding: "utf8" }),
  crlfDelay: Infinity,
});
// Inline data, not from a sample file. The number of lines the program is willing to read.
const limit = 10;
let read = 0;
let parsed = 0;
let stopped = false;
for await (const line of reader) {
  if (read === limit) {
    stopped = true;
    break;
  }
  read++;
  try {
    JSON.parse(line);
    parsed++;
  } catch (error) {
    // A line that does not parse is counted as read, and it uses up the limit.
  }
}
reader.close();
console.log(`Lines read: ${read}`);
console.log(`Records parsed: ${parsed}`);
console.log(`Stopped at the limit: ${stopped ? "yes" : "no"}`);
```
~~~

The output is the same in every language:

~~~text
Lines read: 10
Records parsed: 9
Stopped at the limit: yes
~~~

Ten lines were read, and nine of them parsed. The eleventh line is the one that triggers the stop: the loop fetches it, finds the limit reached, and leaves without parsing it. The stop is recorded in the report, so a downstream step can tell a complete read from a truncated one.

> **Aside: the limit belongs to the reader, not the file.**
> A file that is longer than the limit is not an error in itself. The reader's job is to say that it stopped, so the caller can decide whether a partial read is acceptable.

> **Common mistake.** Reading a stream into a list and then cutting the list to the limit. The whole stream has already been loaded by then. Stop the loop at the limit, as the samples do.

---
