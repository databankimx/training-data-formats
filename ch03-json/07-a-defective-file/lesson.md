# A Defective File

The file `customers-truncated.json` is the start of the customer array, cut off partway through. It was made the way real files get damaged: an export was interrupted, a disk was full, or a transfer stopped before the end. The sample reads the file, and checks two things. Does the parser accept it? Does the file at least start like JSON?

A parser stops at the first error, and it doesn't keep going to find the next valid part. A truncated file therefore fails at the end, and nothing in the parser's result says where the good data stopped. Each language reports the failure differently, so the sample doesn't print the message. It only says whether the file parsed.

The starting bracket is a separate question. Detection in Chapter 2 looks at the first bytes. A file that starts with a bracket is JSON, even if it's damaged. The sample reports both answers, so the two questions stay apart.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// The sample file is read from the folder named by TRAINING_DATA. The parse is tried, and a failure is caught rather than shown as a crash.
using System.Text.Json;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers-truncated.json");
var text = File.ReadAllText(path, System.Text.Encoding.UTF8);
var valid = true;
try
{
    using var document = JsonDocument.Parse(text);
}
catch (JsonException)
{
    valid = false;
}
var validText = valid ? "yes" : "no";
var bracketText = text.TrimStart().StartsWith('[') ? "yes" : "no";
Console.WriteLine($"Valid JSON: {validText}");
Console.WriteLine($"Starts with a bracket: {bracketText}");
```
```python
import json
import os

# The sample file is read from the folder named by TRAINING_DATA. The parse is tried, and a failure is caught rather than shown as a crash.
path = os.path.join(os.environ["TRAINING_DATA"], "customers-truncated.json")
with open(path, encoding="utf-8") as handle:
    text = handle.read()
try:
    json.loads(text)
    valid = True
except json.JSONDecodeError:
    valid = False
print(f"Valid JSON: {'yes' if valid else 'no'}")
print(f"Starts with a bracket: {'yes' if text.lstrip().startswith('[') else 'no'}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";

// The sample file is read from the folder named by TRAINING_DATA. The parse is tried, and a failure is caught rather than shown as a crash.
const text = readFileSync(path.join(process.env.TRAINING_DATA, "customers-truncated.json"), "utf8");
let valid = true;
try {
  JSON.parse(text);
} catch (error) {
  valid = false;
}
console.log(`Valid JSON: ${valid ? "yes" : "no"}`);
console.log(`Starts with a bracket: ${text.trimStart().startsWith("[") ? "yes" : "no"}`);
```
~~~

The output is the same in every language:

~~~text
Valid JSON: no
Starts with a bracket: yes
~~~

The first line says the file doesn't parse, which is true. The second says it starts like JSON, which is also true. Neither answer is a repair. The data after the cut is gone, and no parser can recover it, so the honest response is to report the file as incomplete and ask for it again.

Each language's exception is different. C# throws a `JsonException`, Python raises `json.JSONDecodeError`, and JavaScript throws a `SyntaxError`. The sample catches the one that matches, so an unrelated error, such as a missing file, is not hidden. The catch blocks name the exception on purpose.

> **Aside: why not print the error message?**
> The messages differ by language and by version, and the position they give is a byte or character offset that depends on the parser. Printing one would tie the lesson to a particular runtime. The sample reports the answer, which doesn't change.

> **Common mistake.** Catching every exception and reporting the file as invalid. A missing file, a permission error, and a truncated file all look the same in that case, and they need different fixes. Catch the parse error only.

---
