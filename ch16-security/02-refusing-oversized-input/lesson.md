# Refusing Oversized Input

The first defence is a limit on size, checked before the file is read. This sample asks the operating system for the size of `customers.csv`, and compares it with two limits. The first limit is one hundred bytes, which is far smaller than the file, so the file is refused. The second is one megabyte, which the file is within, so it is accepted. The two results show that the check decides, not the file.

The check uses the size the file system reports, so no part of the file is read before the decision. A program that reads a file and then counts its bytes has already used the memory the limit was meant to protect.

The limits here are written in the code, and each one is a decision about what the program will accept. A limit that is too generous protects nothing, and one that is too strict refuses good data, so the value belongs in the program's documentation with the reason for it.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// The sample file's size is checked against two limits before it is read. The check decides, not the content.
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers.csv");
var size = new FileInfo(path).Length;
// Inline data, not from a sample file. A tight limit, far below the file, and a generous one that the file is within.
const long tightLimit = 100;
const long generousLimit = 1024 * 1024;
Console.WriteLine(size > tightLimit
    ? $"Refused: the file is larger than {tightLimit} bytes"
    : "Accepted at the tight limit");
Console.WriteLine(size > generousLimit
    ? $"Refused: the file is larger than {generousLimit} bytes"
    : "Accepted: the file is within the limit");
```
```python
import os

# The sample file's size is checked against two limits before it is read. The check decides, not the content.
path = os.path.join(os.environ["TRAINING_DATA"], "customers.csv")
size = os.path.getsize(path)
# Inline data, not from a sample file. A tight limit, far below the file, and a generous one that the file is within.
tight_limit = 100
generous_limit = 1024 * 1024
print(f"Refused: the file is larger than {tight_limit} bytes" if size > tight_limit else "Accepted at the tight limit")
print("Accepted: the file is within the limit" if size <= generous_limit else f"Refused: the file is larger than {generous_limit} bytes")
```
```javascript
import { statSync } from "node:fs";
import path from "node:path";

// The sample file's size is checked against two limits before it is read. The check decides, not the content.
const size = statSync(path.join(process.env.TRAINING_DATA, "customers.csv")).size;
// Inline data, not from a sample file. A tight limit, far below the file, and a generous one that the file is within.
const tightLimit = 100;
const generousLimit = 1024 * 1024;
console.log(size > tightLimit ? `Refused: the file is larger than ${tightLimit} bytes` : "Accepted at the tight limit");
console.log(size <= generousLimit ? "Accepted: the file is within the limit" : `Refused: the file is larger than ${generousLimit} bytes`);
```
~~~

The output is the same in every language:

~~~text
Refused: the file is larger than 100 bytes
Accepted: the file is within the limit
~~~

The file is more than a hundred bytes, so the tight limit refuses it, and it is well under a megabyte, so the generous limit accepts it. The message names the limit, so whoever reads the log sees why the file was refused and what the limit was, without the file's contents.

> **Aside: the size is the file system's figure.**
> The size is read from the file's metadata, not by counting bytes. That is what makes the check cheap, and it is also why a compressed file's size is its compressed size. The expanded size needs its own check, and the next samples apply that check to the number of records.

> **Common mistake.** Reading the file to find out how big it is. Ask the file system first. A file that passes the check is then read once, and a file that fails is never read at all.

---
