# Writing JSON Lines

Writing JSON Lines is a loop too. For each record, the program serializes it to a single line and writes the line, followed by a newline. Because each record stands alone, the writer never has to go back to change an earlier one, and a log can keep growing for as long as the program runs.

The sample below writes three customers this way, in the compact form that JSON Lines usually uses. The records are typed into the code, so the data is inline, and the comment says so. Compact means no spaces after colons and commas. It keeps each record short, and it's the form most JSON Lines readers expect, though every reader accepts the spaced form too.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// Inline data, not from a sample file. Three customers, typed into the code, written one per line in compact form.
using System.Text.Json;
var customers = new[]
{
    new { customer_id = 1001, name = "Alice Carter", active = true },
    new { customer_id = 1002, name = "Chidi Okafor", active = false },
    new { customer_id = 1003, name = "Mei Lin", active = true },
};
foreach (var customer in customers)
{
    Console.WriteLine(JsonSerializer.Serialize(customer));
}
```
```python
import json

# Inline data, not from a sample file. Three customers, typed into the code, written one per line in compact form.
customers = [
    {"customer_id": 1001, "name": "Alice Carter", "active": True},
    {"customer_id": 1002, "name": "Chidi Okafor", "active": False},
    {"customer_id": 1003, "name": "Mei Lin", "active": True},
]
for customer in customers:
    print(json.dumps(customer, separators=(",", ":")))
```
```javascript
// Inline data, not from a sample file. Three customers, typed into the code, written one per line in compact form.
const customers = [
  { customer_id: 1001, name: "Alice Carter", active: true },
  { customer_id: 1002, name: "Chidi Okafor", active: false },
  { customer_id: 1003, name: "Mei Lin", active: true },
];
for (const customer of customers) {
  console.log(JSON.stringify(customer));
}
```
~~~

The output is the same in every language:

~~~text
{"customer_id":1001,"name":"Alice Carter","active":true}
{"customer_id":1002,"name":"Chidi Okafor","active":false}
{"customer_id":1003,"name":"Mei Lin","active":true}
~~~

Each record is one line, and there are no commas between lines. Read the output in your head as a file: three lines, each a complete value, and a newline after the last one. A reader that gets exactly this text can parse every line on its own.

The writer's job includes one guarantee. A value containing a newline, such as a note with two lines in it, has to be written with the newline escaped as `\n`. Every standard JSON writer does that, and it's the reason the format works. If you build the line yourself by joining strings, the guarantee is yours to keep, and it's easy to lose.

> **Aside: append, don't rewrite.**
> Because the lines are independent, a program that adds a record can open the file in append mode and write one line. It doesn't need to read the file first, which matters for a log that's written all day.

> **Common mistake.** Writing a JSON array, with brackets and commas, into a file named `.jsonl`. Some readers will accept it and others will fail on the first line. The format is one value per line, with no outer structure.

---
