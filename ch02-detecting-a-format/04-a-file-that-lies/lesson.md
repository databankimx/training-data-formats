# A File That Lies

The sample file `customers-as-json.csv` is in the data folder under a `.csv` name. It is not CSV. It holds the first three customers as JSON, which is what happens when a JSON export is saved under the wrong name, or a script writes the wrong kind of output to a file it has named for another.

The sample below reads the name and the content, and prints what each one says. The name gives its extension. The content gives the kind, from the signature rules. It also prints the first line of the content, so you can see the bracket that gives the file away.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// The file is read from the folder named by TRAINING_DATA. Its name says csv, and its content does not.
var name = "customers-as-json.csv";
var bytes = File.ReadAllBytes(Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), name));
var text = System.Text.Encoding.UTF8.GetString(bytes);
var firstLine = text.Split('\n')[0];
var kind = firstLine.TrimStart().StartsWith('[') ? "json" : "not json";
Console.WriteLine($"Name says: {Path.GetExtension(name).TrimStart('.')}");
Console.WriteLine($"Content says: {kind}");
Console.WriteLine($"First line: {firstLine}");
```
```python
import os

# The file is read from the folder named by TRAINING_DATA. Its name says csv, and its content does not.
name = "customers-as-json.csv"
with open(os.path.join(os.environ["TRAINING_DATA"], name), "rb") as handle:
    text = handle.read().decode("utf-8")
first_line = text.split("\n")[0]
print(f"Name says: {os.path.splitext(name)[1][1:]}")
print(f"Content says: {'json' if first_line.lstrip().startswith('[') else 'not json'}")
print(f"First line: {first_line}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";

// The file is read from the folder named by TRAINING_DATA. Its name says csv, and its content does not.
const name = "customers-as-json.csv";
const text = readFileSync(path.join(process.env.TRAINING_DATA, name), "utf8");
const firstLine = text.split("\n")[0];
console.log(`Name says: ${path.extname(name).slice(1)}`);
console.log(`Content says: ${firstLine.trimStart().startsWith("[") ? "json" : "not json"}`);
console.log(`First line: ${firstLine}`);
```
~~~

The output is the same in every language:

~~~text
Name says: csv
Content says: json
First line: [
~~~

The first line of the file is a single bracket, so the content is a JSON array. The name says the file is CSV. A reader that trusts the name would split the first line on commas, find no commas, and report one column with a very strange name. The error would show up in the header, not at the point where the wrong reader was chosen.

The fix is to take the kind from the content, and to tell the person who sent the file that its name is wrong. A detector can't rename the file. It can refuse to read a file as CSV when the content says otherwise, and report the mismatch.

> **Aside: a file can be right and still be named wrong.**
> The content is valid JSON, so nothing about the data is damaged. Only the label is wrong. Fixing the label fixes the problem, and reading the file as JSON is the correct response.

> **Common mistake.** Reading a file as the format its name suggests, because the name is what you expected. When a file doesn't parse, look at its first bytes before you look at the parser.

---
