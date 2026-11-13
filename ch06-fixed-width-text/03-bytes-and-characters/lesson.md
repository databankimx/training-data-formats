# Bytes and Characters

A layout gives positions, and a position is a count of something. Most layouts count characters, but many legacy systems count bytes, and the two agree only while every character is one byte. In UTF-8, a letter such as `é` takes two bytes. Any field after it, on the same line, moves one position to the right when the line is measured in bytes.

Customer 1003 is `Renée Dubois`, and the `é` is in her name. The name is cut at positions 8 to 27, and the balance after it is at positions 40 to 47. In characters, the balance is `980.10`. The sample below cuts the same positions from the same line two ways: as characters, which is what the layout means, and as bytes, which is what a byte-based reader would do.

The sample reads the file's bytes, takes line three, which is customer 1003, and prints the balance both ways.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// The sample file is read from the folder named by TRAINING_DATA. Line three is customer 1003, whose name has an accented letter.
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers.fixed");
var lines = File.ReadAllLines(path, System.Text.Encoding.UTF8);
var line = lines[2];
var byCharacters = line.Substring(39, 8).Trim();
var lineBytes = System.Text.Encoding.UTF8.GetBytes(line);
var byBytes = System.Text.Encoding.UTF8.GetString(lineBytes, 39, 8).Trim();
Console.WriteLine($"By characters: {byCharacters}");
Console.WriteLine($"By bytes: {byBytes}");
```
```python
import os

# The sample file is read from the folder named by TRAINING_DATA. Line three is customer 1003, whose name has an accented letter.
path = os.path.join(os.environ["TRAINING_DATA"], "customers.fixed")
with open(path, encoding="utf-8", newline="") as handle:
    lines = handle.read().splitlines()
line = lines[2]
by_characters = line[39:47].strip()
by_bytes = line.encode("utf-8")[39:47].decode("utf-8").strip()
print(f"By characters: {by_characters}")
print(f"By bytes: {by_bytes}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";

// The sample file is read from the folder named by TRAINING_DATA. Line three is customer 1003, whose name has an accented letter.
const lines = readFileSync(path.join(process.env.TRAINING_DATA, "customers.fixed"), "utf8").split("\n").filter((text) => text !== "");
const line = lines[2];
const byCharacters = line.slice(39, 47).trim();
const byBytes = Buffer.from(line, "utf8").subarray(39, 47).toString("utf8").trim();
console.log(`By characters: ${byCharacters}`);
console.log(`By bytes: ${byBytes}`);
```
~~~

The output is the same in every language:

~~~text
By characters: 980.10
By bytes: 980.1
~~~

The character cut gives the balance as written. The byte cut is shifted one character to the left, because the `é` before it used two bytes. It starts on a space, which the trim removes, and it ends one character early, so it loses the final zero. The result is `980.1`, which is a different number, and nothing reports it.

This is why the layout's unit matters. If the layout counts characters, a byte-based reader gets every field after an accented letter wrong. If it counts bytes, a character-based reader gets the same wrong result. The file itself doesn't say which, so the layout has to.

> **Aside: why the names carried the damage.**
> The accented names are in the file because they are real data. A fixed-width feed with only ASCII names would never show the problem, and it would fail the day a name arrived with an accent.

> **Common mistake.** Testing a fixed-width reader only with ASCII names, and assuming the positions hold for all data. The test passes, and the first accented name in production shifts every later field.

---
