# Reading Fixed-Width Text

Reading a fixed-width file means cutting each line into fields by position. Each field is a substring: the start is the layout's start minus one, and the length is the layout's width. Then the padding is trimmed from the value. The sample below does that for the first customer, using the layout from the first step.

The layout's positions count from one, and string functions count from zero. The customer identifier is at positions 1 to 6, so in code it's characters 0 to 5. The name is at 8 to 27, so it's characters 7 to 26, and the balance is at 40 to 47, so it's characters 39 to 46. Those are the numbers the sample uses.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// The sample file is read from the folder named by TRAINING_DATA. Each field is cut from its layout position, then trimmed.
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers.fixed");
var lines = File.ReadAllLines(path, System.Text.Encoding.UTF8);
var first = lines[0];
var id = first.Substring(0, 6).Trim();
var name = first.Substring(7, 20).Trim();
var balance = first.Substring(39, 8).Trim();
Console.WriteLine($"Records: {lines.Length}");
Console.WriteLine($"First customer: {id} {name} {balance}");
```
```python
import os

# The sample file is read from the folder named by TRAINING_DATA. Each field is cut from its layout position, then trimmed.
path = os.path.join(os.environ["TRAINING_DATA"], "customers.fixed")
with open(path, encoding="utf-8", newline="") as handle:
    lines = handle.read().splitlines()
first = lines[0]
customer_id = first[0:6].strip()
name = first[7:27].strip()
balance = first[39:47].strip()
print(f"Records: {len(lines)}")
print(f"First customer: {customer_id} {name} {balance}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";

// The sample file is read from the folder named by TRAINING_DATA. Each field is cut from its layout position, then trimmed.
const lines = readFileSync(path.join(process.env.TRAINING_DATA, "customers.fixed"), "utf8").split("\n").filter((line) => line !== "");
const first = lines[0];
const customerId = first.slice(0, 6).trim();
const name = first.slice(7, 27).trim();
const balance = first.slice(39, 47).trim();
console.log(`Records: ${lines.length}`);
console.log(`First customer: ${customerId} ${name} ${balance}`);
```
~~~

The output is the same in every language:

~~~text
Records: 12
First customer: 1001 Alice Carter 1250.75
~~~

The three cuts are the whole reader. Each one names a range of positions, and each one trims the padding from the value. The identifier is right-aligned, so its leading spaces are trimmed away, and the balance is right-aligned in the same way. The name is left-aligned, so its trailing spaces go.

Notice the lengths. C#'s `Substring` takes a start and a length, while Python's slice and JavaScript's `slice` take a start and an end. A slice of `first[39:47]` has the same eight characters as `Substring(39, 8)`. Mixing the two forms is a common source of an off-by-one error, so check the end position in whichever form you use.

The file is read as text, so each position is a character. This sample is ASCII in the first line, so characters and bytes agree here. The next sample shows the case where they don't.

> **Aside: the reader trusts the layout, not the data.**
> Every field is cut from the same positions in every line. If one line is shifted, the cut still happens, and it produces a value from the wrong place. The reader can't tell, so the check has to be on the line's length and the field's content.

> **Common mistake.** Cutting the fields without trimming them, and then comparing the identifier with `"1001"`. The padding is part of the value, so the comparison fails with no error, and the lookup finds nothing.

---
