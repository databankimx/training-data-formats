# Writing JSON

Writing reverses reading. The program has a value, a list or an object with fields, and it turns that into text that another program can parse. Each language has a function for this, and each function has options for layout. The options matter: a compact line is cheap to send, and an indented one is easy to read and review.

The sample below builds one customer in the code, writes it as JSON with two-space indentation, and prints the result. The customer is typed into the code, so the data is inline, and the comment says so. It has a null middle name, a list of two tags, and an empty list, so each kind of value shows up in the output.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// Inline data, not from a sample file. One customer, typed into the code, with a null and an empty list among its values.
using System.Text.Json;
var customer = new
{
    customer_id = 1001,
    name = "Alice Carter",
    active = true,
    middle_name = (string)null,
    tags = new[] { "vip", "newsletter" },
    empty_tags = Array.Empty<string>(),
};
var options = new JsonSerializerOptions { WriteIndented = true };
Console.WriteLine(JsonSerializer.Serialize(customer, options));
```
```python
import json

# Inline data, not from a sample file. One customer, typed into the code, with a null and an empty list among its values.
customer = {
    "customer_id": 1001,
    "name": "Alice Carter",
    "active": True,
    "middle_name": None,
    "tags": ["vip", "newsletter"],
    "empty_tags": [],
}
print(json.dumps(customer, indent=2))
```
```javascript
// Inline data, not from a sample file. One customer, typed into the code, with a null and an empty list among its values.
const customer = {
  customer_id: 1001,
  name: "Alice Carter",
  active: true,
  middle_name: null,
  tags: ["vip", "newsletter"],
  empty_tags: [],
};
console.log(JSON.stringify(customer, null, 2));
```
~~~

The output is the same in every language:

~~~text
{
  "customer_id": 1001,
  "name": "Alice Carter",
  "active": true,
  "middle_name": null,
  "tags": [
    "vip",
    "newsletter"
  ],
  "empty_tags": []
}
~~~

Three details are worth noticing. The number `1001` is written without quotes, because it's a number in the program, and a string would be written as `"1001"`. The null is written as `null`, not as an empty string, so a reader can still tell a missing middle name from a blank one. And the empty list is written as `[]` on one line, which every language does, so the output stays readable.

The writer also decides how to write each value. A value that came from arithmetic can carry digits the program never meant to keep: `0.1 + 0.2` is `0.30000000000000004` in most languages, and that is what the writer faithfully records. Chapter 3's homework returns to money for that reason.

> **Aside: the key order is the order you wrote.**
> JSON objects have no defined order, but all three writers keep the order the program used. Other tools may not, so a file compared by bytes can change when a different tool writes it.

> **Common mistake.** Building the text by joining strings with quotes and commas. A name with a double quote in it, such as `Ann "Ace" Ryan`, written as `"Ann "Ace" Ryan"`, produces a file no parser will read. Let the JSON writer escape the text.

---
