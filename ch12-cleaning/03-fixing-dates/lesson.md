# Fixing Dates

The file `customers-bad-dates.csv` has three dates that fail the schema, and each needs a different decision. `14/03/2021` can be fixed with certainty, because 14 cannot be a month, so the first part must be the day. `March 14, 2021` can be fixed with certainty too, because the month is named. `2021-02-30` cannot be fixed, because the form is right and the day does not exist, and no rule says which day was meant.

The cleaner applies four rules, in this order, to each date. A date already in the ISO form and on the calendar is left alone. A slash date whose first part is greater than twelve is read as day first. A date with a month name and a known month is converted. Anything else is sent to review with a reason. A slash date with both parts twelve or less is ambiguous, so it is also sent to review and never converted.

The output has one line for each change or review, and two counts. The reasons are part of the output, because a person reading the report needs to know why each row was touched or left.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package CsvHelper@33.1.0

// The sample file is read from the folder named by TRAINING_DATA. Each date is converted only when its meaning is certain.
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
var body = rows.Skip(1).ToList();
// Inline data, not from a sample file. The month names, so a date in words needs no locale.
var months = new Dictionary<string, int>
{
    ["January"] = 1, ["February"] = 2, ["March"] = 3, ["April"] = 4, ["May"] = 5, ["June"] = 6,
    ["July"] = 7, ["August"] = 8, ["September"] = 9, ["October"] = 10, ["November"] = 11, ["December"] = 12,
};
var changed = 0;
var review = 0;
for (var index = 0; index < body.Count; index++)
{
    var before = body[index][column];
    var line = index + 2;
    var after = (string)null;
    var reason = "";
    var iso = Regex.Match(before, @"^(\d{4})-(\d{2})-(\d{2})$");
    var slash = Regex.Match(before, @"^(\d{2})/(\d{2})/(\d{4})$");
    var words = Regex.Match(before, @"^([A-Za-z]+) (\d{1,2}), (\d{4})$");
    if (iso.Success && IsRealDate(before))
    {
        continue;
    }
    if (slash.Success && int.Parse(slash.Groups[1].Value) > 12)
    {
        var day = int.Parse(slash.Groups[1].Value);
        after = IsoOrNull(int.Parse(slash.Groups[3].Value), int.Parse(slash.Groups[2].Value), day);
        reason = $" (day first, because {day} cannot be a month)";
    }
    else if (words.Success && months.ContainsKey(words.Groups[1].Value))
    {
        after = IsoOrNull(int.Parse(words.Groups[3].Value), months[words.Groups[1].Value], int.Parse(words.Groups[2].Value));
        reason = " (month name)";
    }
    if (after != null)
    {
        changed++;
        Console.WriteLine($"Line {line}: signup_date {before} -> {after}{reason}");
    }
    else
    {
        review++;
        var why = iso.Success ? "not a real date" : "not in a recognised form";
        Console.WriteLine($"Line {line}: signup_date {before} needs review ({why})");
    }
}
Console.WriteLine($"Rows changed: {changed}");
Console.WriteLine($"Rows needing review: {review}");

// Returns the ISO form when the year, month, and day make a real date, or null when they do not.
string IsoOrNull(int year, int month, int day)
{
    var text = $"{year:D4}-{month:D2}-{day:D2}";
    return IsRealDate(text) ? text : null;
}

// True when the text is a real date in the ISO form.
bool IsRealDate(string text) => DateTime.TryParseExact(text, "yyyy-MM-dd", CultureInfo.InvariantCulture, DateTimeStyles.None, out _);
```
```python
import csv
import os
import re
from datetime import datetime

# The sample file is read from the folder named by TRAINING_DATA. Each date is converted only when its meaning is certain.
path = os.path.join(os.environ["TRAINING_DATA"], "customers-bad-dates.csv")
with open(path, encoding="utf-8", newline="") as handle:
    rows = list(csv.reader(handle))
column = rows[0].index("signup_date")
body = rows[1:]
# Inline data, not from a sample file. The month names, so a date in words needs no locale.
months = {
    "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
    "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12,
}


def is_real_date(text):
    try:
        datetime.strptime(text, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def iso_or_none(year, month, day):
    text = f"{year:04d}-{month:02d}-{day:02d}"
    return text if is_real_date(text) else None


changed = 0
review = 0
for index, row in enumerate(body):
    before = row[column]
    line = index + 2
    after = None
    reason = ""
    iso = re.fullmatch(r"\d{4}-\d{2}-\d{2}", before)
    slash = re.fullmatch(r"(\d{2})/(\d{2})/(\d{4})", before)
    words = re.fullmatch(r"([A-Za-z]+) (\d{1,2}), (\d{4})", before)
    if iso and is_real_date(before):
        continue
    if slash and int(slash.group(1)) > 12:
        day = int(slash.group(1))
        after = iso_or_none(int(slash.group(3)), int(slash.group(2)), day)
        reason = f" (day first, because {day} cannot be a month)"
    elif words and words.group(1) in months:
        after = iso_or_none(int(words.group(3)), months[words.group(1)], int(words.group(2)))
        reason = " (month name)"
    if after is not None:
        changed += 1
        print(f"Line {line}: signup_date {before} -> {after}{reason}")
    else:
        review += 1
        why = "not a real date" if iso else "not in a recognised form"
        print(f"Line {line}: signup_date {before} needs review ({why})")
print(f"Rows changed: {changed}")
print(f"Rows needing review: {review}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";
import { parse } from "csv-parse/sync";

// The sample file is read from the folder named by TRAINING_DATA. Each date is converted only when its meaning is certain.
const rows = parse(readFileSync(path.join(process.env.TRAINING_DATA, "customers-bad-dates.csv"), "utf8"));
const column = rows[0].indexOf("signup_date");
const body = rows.slice(1);
// Inline data, not from a sample file. The month names, so a date in words needs no locale.
const months = {
  January: 1, February: 2, March: 3, April: 4, May: 5, June: 6,
  July: 7, August: 8, September: 9, October: 10, November: 11, December: 12,
};

// True when the text is a real date in the ISO form.
function isRealDate(text) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(text)) return false;
  const [year, month, day] = text.split("-").map(Number);
  const date = new Date(Date.UTC(year, month - 1, day));
  return date.getUTCMonth() === month - 1 && date.getUTCDate() === day;
}

function isoOrNull(year, month, day) {
  const text = `${String(year).padStart(4, "0")}-${String(month).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
  return isRealDate(text) ? text : null;
}

let changed = 0;
let review = 0;
body.forEach((row, index) => {
  const before = row[column];
  const line = index + 2;
  let after = null;
  let reason = "";
  const iso = /^\d{4}-\d{2}-\d{2}$/.test(before);
  const slash = before.match(/^(\d{2})\/(\d{2})\/(\d{4})$/);
  const words = before.match(/^([A-Za-z]+) (\d{1,2}), (\d{4})$/);
  if (iso && isRealDate(before)) return;
  if (slash && Number(slash[1]) > 12) {
    const day = Number(slash[1]);
    after = isoOrNull(Number(slash[3]), Number(slash[2]), day);
    reason = ` (day first, because ${day} cannot be a month)`;
  } else if (words && words[1] in months) {
    after = isoOrNull(Number(words[3]), months[words[1]], Number(words[2]));
    reason = " (month name)";
  }
  if (after !== null) {
    changed++;
    console.log(`Line ${line}: signup_date ${before} -> ${after}${reason}`);
  } else {
    review++;
    const why = iso ? "not a real date" : "not in a recognised form";
    console.log(`Line ${line}: signup_date ${before} needs review (${why})`);
  }
});
console.log(`Rows changed: ${changed}`);
console.log(`Rows needing review: ${review}`);
```
~~~

The output is the same in every language:

~~~text
Line 2: signup_date 14/03/2021 -> 2021-03-14 (day first, because 14 cannot be a month)
Line 3: signup_date March 14, 2021 -> 2021-03-14 (month name)
Line 4: signup_date 2021-02-30 needs review (not a real date)
Rows changed: 2
Rows needing review: 1
~~~

Two rows were converted and one was sent to review. Rows five and six, `2023-01-18` and `2021-07-22`, are already correct and produce no line. The report makes each decision checkable: a reader can see the original, the new value, and the reason for each.

The review line for `2021-02-30` is not a failure of the cleaner. It is the cleaner declining to invent a date, and the person who owns the data must decide the right day. A cleaner that picked the 28th or the 1st would look helpful and be wrong.

> **Aside: an ambiguous date is a review, not a conversion.**
> `03/04/2021` has both parts twelve or less, so it could be the third of April or the fourth of March. Neither reading can be chosen from the value alone, and the homework uses such a date for that reason.

> **Common mistake.** Parsing a month name with the system locale. A computer set to a French locale reads `March` as an unknown word, so the same program gives different results on different machines. The month names are listed in the code, as the samples do.

---
