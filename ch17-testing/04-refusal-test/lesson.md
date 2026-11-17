# Refusal Test

A refusal test checks that bad input is rejected. The file `customers-truncated.json` is the one from the JSON chapter, cut off partway through, and the test checks that the reader refuses it. A test that only checks refusal is weak, because a reader that refused every file would pass it. So the test also reads `customers.json`, the complete file, and checks that it is accepted.

The two checks together show that the reader distinguishes the two cases. A refusal must be the parser's own error, the one the JSON chapter caught, and not some other failure such as a missing file. The sample catches only that error, so a missing file would stop the test with its own message rather than being counted as a refusal.

The lesson is the pair. Refusal alone proves little, and acceptance alone proves little, but the two together show the boundary is in the right place.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// The truncated file must be refused, and the complete file must be accepted. Only the parser's own error counts as a refusal.
using System.Text.Json;
var folder = Environment.GetEnvironmentVariable("TRAINING_DATA");
var passed = 0;
var failed = 0;
void Check(string label, bool ok)
{
    Console.WriteLine($"{(ok ? "PASS" : "FAIL")}: {label}");
    if (ok) passed++; else failed++;
}
bool Refused(string file)
{
    try
    {
        JsonDocument.Parse(File.ReadAllText(Path.Combine(folder, file), System.Text.Encoding.UTF8));
        return false;
    }
    catch (JsonException)
    {
        return true;
    }
}
Check("the truncated file is refused", Refused("customers-truncated.json"));
Check("the complete file is accepted", !Refused("customers.json"));
Console.WriteLine($"Checks passed: {passed}");
Console.WriteLine($"Checks failed: {failed}");
```
```python
import json
import os

# The truncated file must be refused, and the complete file must be accepted. Only the parser's own error counts as a refusal.
folder = os.environ["TRAINING_DATA"]
passed = 0
failed = 0


def refused(file):
    with open(os.path.join(folder, file), encoding="utf-8") as handle:
        text = handle.read()
    try:
        json.loads(text)
        return False
    except json.JSONDecodeError:
        return True


def check(label, ok):
    global passed, failed
    print(f"{'PASS' if ok else 'FAIL'}: {label}")
    if ok:
        passed += 1
    else:
        failed += 1


check("the truncated file is refused", refused("customers-truncated.json"))
check("the complete file is accepted", not refused("customers.json"))
print(f"Checks passed: {passed}")
print(f"Checks failed: {failed}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";

// The truncated file must be refused, and the complete file must be accepted. Only the parser's own error counts as a refusal.
const folder = process.env.TRAINING_DATA;
let passed = 0;
let failed = 0;
function refused(file) {
  const text = readFileSync(path.join(folder, file), "utf8");
  try {
    JSON.parse(text);
    return false;
  } catch (error) {
    if (error instanceof SyntaxError) return true;
    throw error;
  }
}
function check(label, ok) {
  console.log(`${ok ? "PASS" : "FAIL"}: ${label}`);
  if (ok) passed++;
  else failed++;
}
check("the truncated file is refused", refused("customers-truncated.json"));
check("the complete file is accepted", !refused("customers.json"));
console.log(`Checks passed: ${passed}`);
console.log(`Checks failed: ${failed}`);
```
~~~

The output is the same in every language:

~~~text
PASS: the truncated file is refused
PASS: the complete file is accepted
Checks passed: 2
Checks failed: 0
~~~

The reader refused the truncated file with its own parse error, and it accepted the complete file. Each side of the boundary is checked, so a change that made the reader refuse everything, or accept everything, would fail one of the two checks.

> **Aside: refuse for the right reason.**
> A test that refuses a file for the wrong reason passes by accident. The catch blocks name the parse error, so a missing file, a permission failure, or a bug in the test is not counted as a refusal.

> **Common mistake.** Testing refusal with an empty file or a file of the wrong name. Both are refused for reasons unrelated to the content, and the test shows nothing about the reader's handling of truncated data.

---
