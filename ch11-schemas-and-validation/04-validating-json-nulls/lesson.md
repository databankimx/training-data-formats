# Validating JSON Nulls

The file `customers-null-mix.json` has three records, and each breaks a rule in a different way. Record 1001 has an `email` that is `null`. Record 1002 has an empty `name` and a `tags` value that is `null`. Record 1003 has no `email` key at all. The schema treats these as different problems: a null is present and holds nothing, a missing key is absent, and an empty string is present and holds text with nothing in it. The report keeps those three apart, because each has a different fix.

The validator asks about the key first. For each required field it checks whether the key exists, then whether the value is null, then, for text, whether it is empty. Each language has its own way to ask about a key, as the YAML chapter showed, and the checks are written to use it.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// The sample file is read from the folder named by TRAINING_DATA. Each key is checked for presence, then for null, then for empty text.
using System.Text.Json;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers-null-mix.json");
using var document = JsonDocument.Parse(File.ReadAllText(path, System.Text.Encoding.UTF8));
var records = document.RootElement.EnumerateArray().ToList();
var failing = 0;
foreach (var record in records)
{
    var id = record.GetProperty("customer_id").GetInt64();
    // Inline data, not from a sample file. The schema is these rules: email, name, and tags are required.
    var problems = new List<string>();
    var email = Missing(record, "email");
    if (email != null) problems.Add($"email {email}");
    var name = Missing(record, "name");
    if (name != null) problems.Add($"name {name}");
    else if (record.GetProperty("name").GetString() == "") problems.Add("name is empty");
    var tags = Missing(record, "tags");
    if (tags != null) problems.Add($"tags {tags}");
    foreach (var problem in problems)
    {
        Console.WriteLine($"Record {id}: {problem}");
    }
    if (problems.Count > 0) failing++;
}
Console.WriteLine($"Records checked: {records.Count}");
Console.WriteLine($"Records failing: {failing}");

// Returns "is missing" or "is null" for a key that is absent or null, and null for a key that holds a value.
string Missing(JsonElement record, string key)
{
    if (!record.TryGetProperty(key, out var value)) return "is missing";
    if (value.ValueKind == JsonValueKind.Null) return "is null";
    return null;
}
```
```python
import json
import os

# The sample file is read from the folder named by TRAINING_DATA. Each key is checked for presence, then for None, then for empty text.
path = os.path.join(os.environ["TRAINING_DATA"], "customers-null-mix.json")
with open(path, encoding="utf-8") as handle:
    records = json.load(handle)


def missing(record, key):
    # "in" tells an absent key from a key that holds None.
    if key not in record:
        return "is missing"
    if record[key] is None:
        return "is null"
    return None


failing = 0
for record in records:
    # Inline data, not from a sample file. The schema is these rules: email, name, and tags are required.
    problems = []
    email = missing(record, "email")
    if email:
        problems.append(f"email {email}")
    name = missing(record, "name")
    if name:
        problems.append(f"name {name}")
    elif record["name"] == "":
        problems.append("name is empty")
    tags = missing(record, "tags")
    if tags:
        problems.append(f"tags {tags}")
    for problem in problems:
        print(f"Record {record['customer_id']}: {problem}")
    if problems:
        failing += 1
print(f"Records checked: {len(records)}")
print(f"Records failing: {failing}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";

// The sample file is read from the folder named by TRAINING_DATA. Each key is checked for presence, then for null, then for empty text.
const records = JSON.parse(readFileSync(path.join(process.env.TRAINING_DATA, "customers-null-mix.json"), "utf8"));

// Returns "is missing" for an absent key, "is null" for a null value, and null for a key that holds a value.
function missing(record, key) {
  if (!(key in record)) return "is missing";
  if (record[key] === null) return "is null";
  return null;
}

let failing = 0;
for (const record of records) {
  // Inline data, not from a sample file. The schema is these rules: email, name, and tags are required.
  const problems = [];
  const email = missing(record, "email");
  if (email) problems.push(`email ${email}`);
  const name = missing(record, "name");
  if (name) problems.push(`name ${name}`);
  else if (record.name === "") problems.push("name is empty");
  const tags = missing(record, "tags");
  if (tags) problems.push(`tags ${tags}`);
  for (const problem of problems) {
    console.log(`Record ${record.customer_id}: ${problem}`);
  }
  if (problems.length > 0) failing++;
}
console.log(`Records checked: ${records.length}`);
console.log(`Records failing: ${failing}`);
```
~~~

The output is the same in every language:

~~~text
Record 1001: email is null
Record 1002: name is empty
Record 1002: tags is null
Record 1003: email is missing
Records checked: 3
Records failing: 3
~~~

The four problem lines cover three records, so the failing count is three. Record 1002 has two problems, and both are reported, in the order the rules run. The checks never treat the three cases as one. A null email says the form was filled in with nothing, a missing email says the field was dropped by whatever wrote the file, and an empty name says the value is present and blank. A fix for one of them does not fix the others.

> **Aside: a null in a required field is still a failure.**
> A schema that says a field is required usually means the value must be present and not null. If a field may be null, the schema must say so, and the rule for it is then different. Write the rule that matches what the data means.

> **Common mistake.** Testing a required field with a truthiness check, such as `if record.email`. An empty string, a zero, and a null all fail that test, so the report can't say which problem it is. Test the key, then the value.

---
