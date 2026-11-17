# Filling Nulls

The file `customers-null-mix.json` has three records with missing or empty values, and each needs a different decision. Record 1002 has a `tags` value that is `null`. The data gives that a meaning: a customer with no tags has an empty list, so the cleaner can replace the null with an empty list, and it records the change. Records 1001 and 1003 have an email that is null or missing, and record 1002 has an empty name. None of these has a meaning the data supplies, so each goes to review.

The cleaner handles the record fields in a fixed order: email, name, then tags. Each problem is printed on its own line, with the record identifier. The report then counts two things. A record is changed when it had a value replaced, and a record needs review when any of its fields could not be decided. A record can be both, and it's counted once in each total.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// The sample file is read from the folder named by TRAINING_DATA. A null tags list becomes an empty list, and the rest go to review.
using System.Text.Json;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers-null-mix.json");
using var document = JsonDocument.Parse(File.ReadAllText(path, System.Text.Encoding.UTF8));
var records = document.RootElement.EnumerateArray().ToList();
var changed = 0;
var review = 0;
foreach (var record in records)
{
    var id = record.GetProperty("customer_id").GetInt64();
    var needsReview = false;
    var wasChanged = false;
    // Inline data, not from a sample file. The rules: an email must be present, a name must not be empty, and a null tags list means no tags.
    var email = State(record, "email");
    if (email != null)
    {
        needsReview = true;
        Console.WriteLine($"Record {id}: email {email} needs review");
    }
    var name = State(record, "name");
    if (name != null)
    {
        needsReview = true;
        Console.WriteLine($"Record {id}: name {name} needs review");
    }
    else if (record.GetProperty("name").GetString() == "")
    {
        needsReview = true;
        Console.WriteLine($"Record {id}: name is empty needs review");
    }
    var tags = State(record, "tags");
    if (tags == "is null")
    {
        wasChanged = true;
        Console.WriteLine($"Record {id}: tags is null replaced with empty list");
    }
    else if (tags != null)
    {
        needsReview = true;
        Console.WriteLine($"Record {id}: tags {tags} needs review");
    }
    if (wasChanged) changed++;
    if (needsReview) review++;
}
Console.WriteLine($"Records changed: {changed}");
Console.WriteLine($"Records needing review: {review}");

// Returns "is missing" or "is null" for a key that is absent or null, and null for a key that holds a value.
string State(JsonElement record, string key)
{
    if (!record.TryGetProperty(key, out var value)) return "is missing";
    if (value.ValueKind == JsonValueKind.Null) return "is null";
    return null;
}
```
```python
import json
import os

# The sample file is read from the folder named by TRAINING_DATA. A null tags list becomes an empty list, and the rest go to review.
path = os.path.join(os.environ["TRAINING_DATA"], "customers-null-mix.json")
with open(path, encoding="utf-8") as handle:
    records = json.load(handle)


def state(record, key):
    # "in" tells an absent key from a key that holds None.
    if key not in record:
        return "is missing"
    if record[key] is None:
        return "is null"
    return None


changed = 0
review = 0
for record in records:
    record_id = record["customer_id"]
    needs_review = False
    was_changed = False
    # Inline data, not from a sample file. The rules: an email must be present, a name must not be empty, and a null tags list means no tags.
    email = state(record, "email")
    if email:
        needs_review = True
        print(f"Record {record_id}: email {email} needs review")
    name = state(record, "name")
    if name:
        needs_review = True
        print(f"Record {record_id}: name {name} needs review")
    elif record["name"] == "":
        needs_review = True
        print(f"Record {record_id}: name is empty needs review")
    tags = state(record, "tags")
    if tags == "is null":
        was_changed = True
        print(f"Record {record_id}: tags is null replaced with empty list")
    elif tags:
        needs_review = True
        print(f"Record {record_id}: tags {tags} needs review")
    if was_changed:
        changed += 1
    if needs_review:
        review += 1
print(f"Records changed: {changed}")
print(f"Records needing review: {review}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";

// The sample file is read from the folder named by TRAINING_DATA. A null tags list becomes an empty list, and the rest go to review.
const records = JSON.parse(readFileSync(path.join(process.env.TRAINING_DATA, "customers-null-mix.json"), "utf8"));

// Returns "is missing" for an absent key, "is null" for a null value, and null for a key that holds a value.
function state(record, key) {
  if (!(key in record)) return "is missing";
  if (record[key] === null) return "is null";
  return null;
}

let changed = 0;
let review = 0;
for (const record of records) {
  const id = record.customer_id;
  let needsReview = false;
  let wasChanged = false;
  // Inline data, not from a sample file. The rules: an email must be present, a name must not be empty, and a null tags list means no tags.
  const email = state(record, "email");
  if (email) {
    needsReview = true;
    console.log(`Record ${id}: email ${email} needs review`);
  }
  const name = state(record, "name");
  if (name) {
    needsReview = true;
    console.log(`Record ${id}: name ${name} needs review`);
  } else if (record.name === "") {
    needsReview = true;
    console.log(`Record ${id}: name is empty needs review`);
  }
  const tags = state(record, "tags");
  if (tags === "is null") {
    wasChanged = true;
    console.log(`Record ${id}: tags is null replaced with empty list`);
  } else if (tags) {
    needsReview = true;
    console.log(`Record ${id}: tags ${tags} needs review`);
  }
  if (wasChanged) changed++;
  if (needsReview) review++;
}
console.log(`Records changed: ${changed}`);
console.log(`Records needing review: ${review}`);
```
~~~

The output is the same in every language:

~~~text
Record 1001: email is null needs review
Record 1002: name is empty needs review
Record 1002: tags is null replaced with empty list
Record 1003: email is missing needs review
Records changed: 1
Records needing review: 3
~~~

Record 1002 is the only changed record, and it is counted once in that total. All three records need review, and record 1002 appears in both totals because it has a change and a review in the same record. The replaced tags value is recorded on its own line, so a reader can see that the cleaner, not the source, supplied the empty list.

The line for record 1002 that needs review is about its name, not its tags. The name is empty, and the cleaner cannot tell whether the customer's name is unknown or simply not entered, so the record goes to a person.

> **Aside: a rule for a null is a claim about the data.**
> Replacing a null tags list with an empty list is a claim that the source meant no tags. That claim is true for this file, because the other records use empty lists the same way. The rule belongs in the cleaner's documentation, so the claim can be questioned.

> **Common mistake.** Replacing every null with an empty string so the field passes a text rule. An empty string is a value, and it now hides the null. Decide per field what a null means, and keep the null where the meaning is unknown.

---
