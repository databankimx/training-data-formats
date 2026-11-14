# Golden-File Test

A golden file is an expected output that is stored, and each test run compares the program's output with it. The golden text here is inline, so it can be read in the lesson. In a real project it would be a file kept beside the test, and changed only when a person has reviewed the change.

The fixture is a single customer built in the code, with the balance as text, so the golden text is the same in every language. The test writes the customer as compact JSON and compares the result with the golden text. A second check is the one that makes the comparison trustworthy. It changes one character of a copy of the golden text and confirms that the comparison now reports a difference. A comparison that could not report a difference would pass every time, so the second check shows the first one is working.

When a golden test fails, the answer is not always to update the golden file. The change may be a bug, and the test has found it. The golden file is updated only after the change has been reviewed and judged correct.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// Inline data, not from a sample file. The golden text is the expected output, stored beside the test.
using System.Text.Json;
var golden = "{\"customer_id\":1001,\"name\":\"Alice Carter\",\"balance\":\"1250.75\",\"tags\":[\"vip\",\"newsletter\"]}";
var actual = JsonSerializer.Serialize(new
{
    customer_id = 1001,
    name = "Alice Carter",
    balance = "1250.75",
    tags = new[] { "vip", "newsletter" },
});
var passed = 0;
var failed = 0;
void Check(string label, bool ok)
{
    Console.WriteLine($"{(ok ? "PASS" : "FAIL")}: {label}");
    if (ok) passed++; else failed++;
}
Check("output matches the golden text", actual == golden);
// A copy of the golden text with one character changed must not match, or the comparison could never fail.
var changed = golden.Replace("1250.75", "1250.76");
Check("a changed golden text is detected", actual != changed);
Console.WriteLine($"Checks passed: {passed}");
Console.WriteLine($"Checks failed: {failed}");
```
```python
import json

# Inline data, not from a sample file. The golden text is the expected output, stored beside the test.
golden = '{"customer_id":1001,"name":"Alice Carter","balance":"1250.75","tags":["vip","newsletter"]}'
actual = json.dumps(
    {"customer_id": 1001, "name": "Alice Carter", "balance": "1250.75", "tags": ["vip", "newsletter"]},
    separators=(",", ":"),
)
passed = 0
failed = 0


def check(label, ok):
    global passed, failed
    print(f"{'PASS' if ok else 'FAIL'}: {label}")
    if ok:
        passed += 1
    else:
        failed += 1


check("output matches the golden text", actual == golden)
# A copy of the golden text with one character changed must not match, or the comparison could never fail.
changed = golden.replace("1250.75", "1250.76")
check("a changed golden text is detected", actual != changed)
print(f"Checks passed: {passed}")
print(f"Checks failed: {failed}")
```
```javascript
// Inline data, not from a sample file. The golden text is the expected output, stored beside the test.
const golden = '{"customer_id":1001,"name":"Alice Carter","balance":"1250.75","tags":["vip","newsletter"]}';
const actual = JSON.stringify({ customer_id: 1001, name: "Alice Carter", balance: "1250.75", tags: ["vip", "newsletter"] });
let passed = 0;
let failed = 0;
function check(label, ok) {
  console.log(`${ok ? "PASS" : "FAIL"}: ${label}`);
  if (ok) passed++;
  else failed++;
}
check("output matches the golden text", actual === golden);
// A copy of the golden text with one character changed must not match, or the comparison could never fail.
const changed = golden.replace("1250.75", "1250.76");
check("a changed golden text is detected", actual !== changed);
console.log(`Checks passed: ${passed}`);
console.log(`Checks failed: ${failed}`);
```
~~~

The output is the same in every language:

~~~text
PASS: output matches the golden text
PASS: a changed golden text is detected
Checks passed: 2
Checks failed: 0
~~~

The output matches the golden text byte for byte, because the fixture, the golden text, and the serializer's key order all agree. The second check passes because a changed copy does not match, which is what a working comparison should do.

> **Aside: the golden file is a claim, and it needs a reviewer.**
> When a golden test fails after a change to the program, the question is whether the change is right. Updating the golden file is the answer to that question only after someone has looked.

> **Common mistake.** Writing the golden file by running the program and saving its output. That makes the test agree with the program by construction. Check the golden text by hand, as this lesson does, before trusting it.

---
