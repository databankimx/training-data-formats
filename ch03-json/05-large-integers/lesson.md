# Large Integers

The file `customers-big-numbers.json` holds two account numbers. The first is `9007199254740993`, which is 2 to the power of 53, plus one. The second is `12345678901234567890`, which is bigger than the largest value a 64-bit integer can hold. Both are valid JSON, and a parser has to decide what to keep.

JavaScript's numbers are 64-bit floating-point values. They hold every integer exactly up to 2 to the power of 53, and the first account is one past that limit. So the value comes back one less than it was written. The sample below reads the file in each language, and prints each account number as the program holds it.

The three languages make different choices, so this sample's output is not the same everywhere. Each block below is the output of one language, and the reason for each is in the text that follows.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// The sample file is read from the folder named by TRAINING_DATA. Each account number is read as a decimal, which holds 28 digits.
using System.Text.Json;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers-big-numbers.json");
using var document = JsonDocument.Parse(File.ReadAllText(path, System.Text.Encoding.UTF8));
foreach (var account in document.RootElement.EnumerateArray())
{
    var number = account.GetProperty("customer_id").GetDecimal();
    Console.WriteLine(number);
}
```
```python
import json
import os

# The sample file is read from the folder named by TRAINING_DATA. Python's integers have no size limit, so every digit is kept.
path = os.path.join(os.environ["TRAINING_DATA"], "customers-big-numbers.json")
with open(path, encoding="utf-8") as handle:
    accounts = json.load(handle)
for account in accounts:
    print(account["customer_id"])
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";

// The sample file is read from the folder named by TRAINING_DATA. JavaScript reads every number as a 64-bit float.
const accounts = JSON.parse(readFileSync(path.join(process.env.TRAINING_DATA, "customers-big-numbers.json"), "utf8"));
for (const account of accounts) {
  console.log(account.customer_id);
}
```
~~~

The output differs by language. Each language's output is shown here:

~~~text
C#:
9007199254740993
12345678901234567890

Python:
9007199254740993
12345678901234567890

JavaScript:
9007199254740992
12345678901234567000
~~~

Python keeps every digit, because its integers have no size limit. C# reads each number as a `decimal`, which holds up to 28 digits, so both values are exact. JavaScript reads each one as a 64-bit float, and the first value becomes `9007199254740992`. The second value becomes `12345678901234567000`, which is the nearest float, and the trailing digits are invented. Neither value is what the file says.

Nothing in the file signals the loss. JavaScript doesn't raise an error, and the printed number looks like a plausible account number. A program that uses these ids to look up records will find the wrong ones, or none.

C# has a choice you might not expect. If the sample asked for `GetInt64`, the first value would be exact, because it fits in a `long`, but the second would throw an error, because it doesn't. Choosing a type is a decision about the data you expect. A `decimal` is wider than a `long` and still exact for whole numbers, so it's a safe default for identifiers that might grow.

> **Aside: why not just use a float everywhere?**
> A float is compact and fast, and it is right for measurements, where a small error is expected. An identifier is different. A one-digit error in an account number is a wrong record, not a rounding difference.

> **Common mistake.** Assuming that a number that parses without error is exact. A parser reports an error for a number that won't fit a type, but for a float it often returns a value that's close without saying so.

---
