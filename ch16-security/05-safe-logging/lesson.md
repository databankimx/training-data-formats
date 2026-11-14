# Safe Logging

Every program logs its problems, and the log is read by people and by tools. The input is the one thing a logger must not trust, because its text is whatever the sender wrote. A value that contains a line break can start a second, false log entry. A value that contains terminal control characters can change what a person sees on screen. A value that contains personal data copies that data into a file that is kept longer than it should be.

The rule is to log the location, the field, and the reason, and to leave out the value. This sample checks the dates in `customers-bad-dates.csv`, which is the file the validation chapter used, and it logs each problem in that form. The log says `signup_date is not YYYY-MM-DD`, not the date itself, so the log is safe to read and the value stays in the file where it can be checked.

The log lines are written by the program, so their structure is the program's, and a reader can rely on each line having the same shape. The count at the end lets a reader check that every problem was logged.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package CsvHelper@33.1.0

// The sample file is read from the folder named by TRAINING_DATA. Each problem is logged with its location and reason, and the value is not logged.
using System.Globalization;
using System.Text.RegularExpressions;
using CsvHelper;
using CsvHelper.Configuration;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers-bad-dates.csv");
var rows = new List<string[]>();
using (var csv = new CsvReader(new StreamReader(path, System.Text.Encoding.UTF8), new CsvConfiguration(CultureInfo.InvariantCulture)))
{
    while (csv.Read())
    {
        rows.Add(csv.Parser.Record);
    }
}
var column = Array.IndexOf(rows[0], "signup_date");
var logged = 0;
for (var line = 1; line < rows.Count; line++)
{
    var value = rows[line][column];
    string reason = null;
    if (!Regex.IsMatch(value, @"^\d{4}-\d{2}-\d{2}$"))
    {
        reason = "not YYYY-MM-DD";
    }
    else if (!DateTime.TryParseExact(value, "yyyy-MM-dd", CultureInfo.InvariantCulture, DateTimeStyles.None, out _))
    {
        reason = "not a real date";
    }
    if (reason != null)
    {
        logged++;
        // The value is not logged, so the log holds only the location and the reason.
        Console.WriteLine($"Line {line + 1}: signup_date is {reason} (value not logged)");
    }
}
Console.WriteLine($"Problems logged: {logged}");
```
```python
import csv
import os
import re
from datetime import datetime

# The sample file is read from the folder named by TRAINING_DATA. Each problem is logged with its location and reason, and the value is not logged.
path = os.path.join(os.environ["TRAINING_DATA"], "customers-bad-dates.csv")
with open(path, encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle))
logged = 0
for line, row in enumerate(rows, start=2):
    value = row["signup_date"]
    reason = None
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        reason = "not YYYY-MM-DD"
    else:
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            reason = "not a real date"
    if reason:
        logged += 1
        # The value is not logged, so the log holds only the location and the reason.
        print(f"Line {line}: signup_date is {reason} (value not logged)")
print(f"Problems logged: {logged}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";
import { parse } from "csv-parse/sync";

// The sample file is read from the folder named by TRAINING_DATA. Each problem is logged with its location and reason, and the value is not logged.
const rows = parse(readFileSync(path.join(process.env.TRAINING_DATA, "customers-bad-dates.csv"), "utf8"), { columns: true });
let logged = 0;
rows.forEach((row, index) => {
  const value = row.signup_date;
  let reason = null;
  const shape = /^\d{4}-\d{2}-\d{2}$/.test(value);
  if (!shape) {
    reason = "not YYYY-MM-DD";
  } else {
    const [year, month, day] = value.split("-").map(Number);
    const date = new Date(Date.UTC(year, month - 1, day));
    if (date.getUTCMonth() !== month - 1 || date.getUTCDate() !== day) reason = "not a real date";
  }
  if (reason) {
    logged++;
    // The value is not logged, so the log holds only the location and the reason.
    console.log(`Line ${index + 2}: signup_date is ${reason} (value not logged)`);
  }
});
console.log(`Problems logged: ${logged}`);
```
~~~

The output is the same in every language:

~~~text
Line 2: signup_date is not YYYY-MM-DD (value not logged)
Line 3: signup_date is not YYYY-MM-DD (value not logged)
Line 4: signup_date is not a real date (value not logged)
Problems logged: 3
~~~

Three problems are logged, each with its line, its field, and its reason, and none with the date that caused it. A reader can find the line in the file, and the file still holds the values. The log contains no text from the input, so a value with a line break or a control character could not change the shape of the log.

> **Aside: the log is an output, and it is read by others.**
> Anything written to the log can reach a person, a monitoring tool, or a third party. Treat it with the same care as a report, and leave out what the report does not need.

> **Common mistake.** Logging the whole input line so that the problem can be found. The line is the same untrusted text, and a value with a line break in it can write a second, false entry. Log the line number, and let the reader look at the file.

---
