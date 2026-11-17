# Validating a Clean File

The validator reads each row of `customers.csv`, runs every rule on it, and collects the problems. The clean file should pass everything, so the output is a count of rows checked and a count of rows failing, with no problem lines. A validator that reports zero failures on a file that should pass is the first check that it works, and the next sample shows the output when it does find problems.

The schema is written in the code as the rules in the first step. Every value is text in a CSV file, so each rule parses or matches the text. The date rule checks the shape first, then the calendar. The duplicate rule keeps a set of identifiers seen so far, which catches a repeated `customer_id` on a later row.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package CsvHelper@33.1.0

// The sample file is read from the folder named by TRAINING_DATA. Every value is text, so each rule checks or parses it.
using System.Globalization;
using System.Text.RegularExpressions;
using CsvHelper;
using CsvHelper.Configuration;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers.csv");
var rows = new List<string[]>();
using (var csv = new CsvReader(new StreamReader(path, System.Text.Encoding.UTF8), new CsvConfiguration(CultureInfo.InvariantCulture)))
{
    while (csv.Read())
    {
        rows.Add(csv.Parser.Record);
    }
}
var header = rows[0];
var body = rows.Skip(1).ToList();
var ids = new HashSet<string>();
var failing = 0;
for (var index = 0; index < body.Count; index++)
{
    var row = body[index];
    // Inline data, not from a sample file. The schema is these rules, one for each column.
    var problems = new List<string>();
    var id = Value(row, "customer_id");
    if (!Regex.IsMatch(id, @"^\d+$")) problems.Add("customer_id is not a whole number");
    if (!ids.Add(id)) problems.Add("customer_id is a duplicate");
    if (string.IsNullOrWhiteSpace(Value(row, "name"))) problems.Add("name is empty");
    if (string.IsNullOrWhiteSpace(Value(row, "email"))) problems.Add("email is empty");
    var date = Value(row, "signup_date");
    if (!Regex.IsMatch(date, @"^\d{4}-\d{2}-\d{2}$")) problems.Add("signup_date is not YYYY-MM-DD");
    else if (!DateTime.TryParseExact(date, "yyyy-MM-dd", CultureInfo.InvariantCulture, DateTimeStyles.None, out _)) problems.Add("signup_date is not a real date");
    if (!Regex.IsMatch(Value(row, "balance"), @"^\d+\.\d{2}$")) problems.Add("balance does not have two decimal places");
    if (Value(row, "active") != "true" && Value(row, "active") != "false") problems.Add("active is not true or false");
    if (!Regex.IsMatch(Value(row, "country_code"), @"^[A-Z]{2}$")) problems.Add("country_code is not two uppercase letters");
    foreach (var problem in problems)
    {
        Console.WriteLine($"Line {index + 2}: {problem}");
    }
    if (problems.Count > 0) failing++;
}
Console.WriteLine($"Rows checked: {body.Count}");
Console.WriteLine($"Rows failing: {failing}");

// Returns the value of a named column in a row.
string Value(string[] row, string column) => row[Array.IndexOf(header, column)];
```
```python
import csv
import os
import re
from datetime import datetime

# The sample file is read from the folder named by TRAINING_DATA. Every value is text, so each rule checks or parses it.
path = os.path.join(os.environ["TRAINING_DATA"], "customers.csv")
with open(path, encoding="utf-8", newline="") as handle:
    rows = list(csv.reader(handle))
header = rows[0]
body = rows[1:]


def is_real_date(text):
    # The shape is checked first, then the calendar, so 2021-02-30 is refused.
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        return "not YYYY-MM-DD"
    try:
        datetime.strptime(text, "%Y-%m-%d")
    except ValueError:
        return "not a real date"
    return None


ids = set()
failing = 0
for index, row in enumerate(body):
    # Inline data, not from a sample file. The schema is these rules, one for each column.
    value = dict(zip(header, row))
    problems = []
    if not re.fullmatch(r"\d+", value["customer_id"]):
        problems.append("customer_id is not a whole number")
    if value["customer_id"] in ids:
        problems.append("customer_id is a duplicate")
    ids.add(value["customer_id"])
    if not value["name"].strip():
        problems.append("name is empty")
    if not value["email"].strip():
        problems.append("email is empty")
    date_problem = is_real_date(value["signup_date"])
    if date_problem:
        problems.append(f"signup_date is {date_problem}")
    if not re.fullmatch(r"\d+\.\d{2}", value["balance"]):
        problems.append("balance does not have two decimal places")
    if value["active"] not in ("true", "false"):
        problems.append("active is not true or false")
    if not re.fullmatch(r"[A-Z]{2}", value["country_code"]):
        problems.append("country_code is not two uppercase letters")
    for problem in problems:
        print(f"Line {index + 2}: {problem}")
    if problems:
        failing += 1
print(f"Rows checked: {len(body)}")
print(f"Rows failing: {failing}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";
import { parse } from "csv-parse/sync";

// The sample file is read from the folder named by TRAINING_DATA. Every value is text, so each rule checks or parses it.
const rows = parse(readFileSync(path.join(process.env.TRAINING_DATA, "customers.csv"), "utf8"));
const header = rows[0];
const body = rows.slice(1);

// Returns null for a real calendar date, or the problem. The shape is checked first, then the calendar.
function dateProblem(text) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(text)) return "not YYYY-MM-DD";
  const [year, month, day] = text.split("-").map(Number);
  const date = new Date(Date.UTC(year, month - 1, day));
  return date.getUTCMonth() === month - 1 && date.getUTCDate() === day ? null : "not a real date";
}

const ids = new Set();
let failing = 0;
body.forEach((row, index) => {
  // Inline data, not from a sample file. The schema is these rules, one for each column.
  const value = Object.fromEntries(header.map((name, column) => [name, row[column]]));
  const problems = [];
  if (!/^\d+$/.test(value.customer_id)) problems.push("customer_id is not a whole number");
  if (ids.has(value.customer_id)) problems.push("customer_id is a duplicate");
  ids.add(value.customer_id);
  if (value.name.trim() === "") problems.push("name is empty");
  if (value.email.trim() === "") problems.push("email is empty");
  const date = dateProblem(value.signup_date);
  if (date) problems.push(`signup_date is ${date}`);
  if (!/^\d+\.\d{2}$/.test(value.balance)) problems.push("balance does not have two decimal places");
  if (value.active !== "true" && value.active !== "false") problems.push("active is not true or false");
  if (!/^[A-Z]{2}$/.test(value.country_code)) problems.push("country_code is not two uppercase letters");
  for (const problem of problems) {
    console.log(`Line ${index + 2}: ${problem}`);
  }
  if (problems.length > 0) failing++;
});
console.log(`Rows checked: ${body.length}`);
console.log(`Rows failing: ${failing}`);
```
~~~

The output is the same in every language:

~~~text
Rows checked: 12
Rows failing: 0
~~~

Twelve rows checked, and none failed. Each rule ran on each row, so a pass means every row met every rule, not that the first row did. The line numbers in the report count the header as line one, so the first data row is line two, and a failing row is reported under that number.

The three versions run the same checks in the same order. The date rule reports one of two problems, and the difference matters: a shape problem means the value was written in the wrong form, and a calendar problem means the form is right but the date is impossible. The next sample shows both.

> **Aside: the rules are checks on the text.**
> In a CSV file a value such as `2021-02-30` is only text. The rules parse it, and the parse is where a calendar problem is found. A parser that accepts any text would pass every row here.

> **Common mistake.** Checking a balance as a number, which accepts `1250.7` and `1250.70` alike. The schema says two decimal places, so the check must look at the text.

---
