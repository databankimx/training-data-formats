# A Short Row

The file `customers-fixed-short-row.fixed` is the customer file with one line cut short. Line three, which is customer 1003, stops at position 30, before the balance and everything after it. Its identifier and name are whole, so the damage is easy to miss in a quick look.

The layout needs every line to be at least 56 characters long, because the last column, the country code, ends at position 56. A line shorter than that doesn't have every field, and the reader has to know it before it cuts.

The sample below reads the file, compares each line's length with the layout's length, and reports each short line. It doesn't cut the line, because the fields after the end are missing and there's nothing to take.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// The sample file is read from the folder named by TRAINING_DATA. Each line is checked against the layout's length before it is cut.
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers-fixed-short-row.fixed");
var lines = File.ReadAllLines(path, System.Text.Encoding.UTF8);
const int layoutLength = 56;
var shortLines = 0;
for (var i = 0; i < lines.Length; i++)
{
    if (lines[i].Length < layoutLength)
    {
        shortLines++;
        Console.WriteLine($"Line {i + 1} has {lines[i].Length} characters, and the layout needs {layoutLength}");
    }
}
Console.WriteLine($"Short lines: {shortLines}");
```
```python
import os

# The sample file is read from the folder named by TRAINING_DATA. Each line is checked against the layout's length before it is cut.
path = os.path.join(os.environ["TRAINING_DATA"], "customers-fixed-short-row.fixed")
with open(path, encoding="utf-8", newline="") as handle:
    lines = handle.read().splitlines()
layout_length = 56
short = 0
for number, line in enumerate(lines, start=1):
    if len(line) < layout_length:
        short += 1
        print(f"Line {number} has {len(line)} characters, and the layout needs {layout_length}")
print(f"Short lines: {short}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";

// The sample file is read from the folder named by TRAINING_DATA. Each line is checked against the layout's length before it is cut.
const lines = readFileSync(path.join(process.env.TRAINING_DATA, "customers-fixed-short-row.fixed"), "utf8").split("\n").filter((line) => line !== "");
const layoutLength = 56;
let short = 0;
lines.forEach((line, index) => {
  if (line.length < layoutLength) {
    short++;
    console.log(`Line ${index + 1} has ${line.length} characters, and the layout needs ${layoutLength}`);
  }
});
console.log(`Short lines: ${short}`);
```
~~~

The output is the same in every language:

~~~text
Line 3 has 30 characters, and the layout needs 56
Short lines: 1
~~~

The report names the line and its length, so a person can find it. The other eleven lines are the full 56 characters, and none of them is reported.

The length check is the step that matters, and the languages handle a missing cut differently. C#'s `Substring` throws an exception when the start and length run past the end of the string, so an unchecked read stops with an error. Python's slice and JavaScript's `slice` return whatever is there, so an unchecked read gives a shorter value and no error. Both are wrong results for the balance, and the second one is the harder to see. The check is the same in each case: test the length first, then cut.

> **Aside: report the short line, do not pad it.**
> Padding the line with spaces would make the balance read as empty, which is a different fact from a missing balance. The reader has to report the damage and leave the decision to a person, as the ragged-row sample did for CSV.

> **Common mistake.** Trusting a fixed-width file because its first lines are full. The short line is in the middle, and only a check on every line finds it.

---
