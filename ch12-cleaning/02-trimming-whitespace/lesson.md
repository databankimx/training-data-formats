# Trimming Whitespace

Whitespace is the most common damage in hand-typed data, and the least visible. A name with two trailing spaces looks correct on screen and fails an exact match. A name with a non-breaking space in the middle looks like a space and is not one. The cleaner fixes both, because the change is certain: a name never needs leading or trailing spaces, and two spaces in a row inside a name are the same as one.

The sample below cleans four names typed into the code. The first has leading and trailing spaces, the second is already clean, the third has a non-breaking space between its words, and the fourth has extra spaces inside it. The report shows each changed value before and after, and it marks the non-breaking space as `<NBSP>`, so the change is visible.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// Inline data, not from a sample file. Four names, typed into the code, with spaces that need cleaning.
using System.Text.RegularExpressions;
var names = new[] { "  Alice Carter  ", "Chidi Okafor", "Mei\u00A0Lin", "Ana   Ribeiro" };
var changed = 0;
for (var index = 0; index < names.Length; index++)
{
    var before = names[index];
    // Inner runs of whitespace become one space, and the ends are trimmed. A non-breaking space counts as whitespace.
    var after = Regex.Replace(before, @"\s+", " ").Trim();
    if (after != before)
    {
        changed++;
        Console.WriteLine($"Line {index + 1}: \"{Visible(before)}\" -> \"{Visible(after)}\"");
    }
}
Console.WriteLine($"Changed values: {changed}");
Console.WriteLine($"Unchanged values: {names.Length - changed}");

// Shows a non-breaking space as <NBSP>, so the change is visible in the report.
string Visible(string text) => text.Replace("\u00A0", "<NBSP>");
```
```python
import re

# Inline data, not from a sample file. Four names, typed into the code, with spaces that need cleaning.
names = ["  Alice Carter  ", "Chidi Okafor", "Mei\u00a0Lin", "Ana   Ribeiro"]


def visible(text):
    # Shows a non-breaking space as <NBSP>, so the change is visible in the report.
    return text.replace("\u00a0", "<NBSP>")


changed = 0
for index, before in enumerate(names, start=1):
    # Inner runs of whitespace become one space, and the ends are trimmed. A non-breaking space counts as whitespace.
    after = re.sub(r"\s+", " ", before).strip()
    if after != before:
        changed += 1
        print(f'Line {index}: "{visible(before)}" -> "{visible(after)}"')
print(f"Changed values: {changed}")
print(f"Unchanged values: {len(names) - changed}")
```
```javascript
// Inline data, not from a sample file. Four names, typed into the code, with spaces that need cleaning.
const names = ["  Alice Carter  ", "Chidi Okafor", "Mei\u00a0Lin", "Ana   Ribeiro"];

// Shows a non-breaking space as <NBSP>, so the change is visible in the report.
function visible(text) {
  return text.replaceAll("\u00a0", "<NBSP>");
}

let changed = 0;
names.forEach((before, index) => {
  // Inner runs of whitespace become one space, and the ends are trimmed. A non-breaking space counts as whitespace.
  const after = before.replace(/\s+/g, " ").trim();
  if (after !== before) {
    changed++;
    console.log(`Line ${index + 1}: "${visible(before)}" -> "${visible(after)}"`);
  }
});
console.log(`Changed values: ${changed}`);
console.log(`Unchanged values: ${names.length - changed}`);
```
~~~

The output is the same in every language:

~~~text
Line 1: "  Alice Carter  " -> "Alice Carter"
Line 3: "Mei<NBSP>Lin" -> "Mei Lin"
Line 4: "Ana   Ribeiro" -> "Ana Ribeiro"
Changed values: 3
Unchanged values: 1
~~~

Three values changed, and the second was left alone because it was already clean. The report shows the value on both sides of each change, so a reader can check that the change is the intended one. Every language treats a non-breaking space as whitespace, so the result is the same in each.

The rule is applied to every value in a column, not only to the ones that look wrong. A clean value passes through unchanged, which is why the count of unchanged values is part of the report.

> **Aside: trim before you compare.**
> A comparison, a duplicate check, or a lookup is only correct when both sides have been cleaned the same way. Trimming one side and not the other makes a match fail with no error.

> **Common mistake.** Trimming with a pattern for an ordinary space only. A non-breaking space, which many editors and web forms insert, survives such a trim and fails the match. Use a whitespace pattern that covers it, as these samples do.

---
