# Summary: Schemas and Validation

This chapter covered schemas: a set of rules for each column, checked against every row, with each failure reported by its location.

## What you learned

- A schema is a list of rules, one set for each column. The rules describe the data, and each format needs its own check of the same rule.
- A validator checks every rule on every row, and reports every failure with its line or record. Stopping at the first failure hides the rest.
- A date rule checks the form and then the calendar. A date such as `2021-02-30` has the right form and is still not a date.
- A null, a missing key, and an empty string are three different problems, and the report keeps them apart.
- A line that is not valid JSON is a failure too. It is reported, and the rest of the file is still checked.
- A count of failing rows is different from a count of problems, because one row can have more than one.

## Quizzes

Three questions, one for each big idea in the chapter. Pick an answer, and read the explanation whichever way it goes.

```quiz
A validator stops at the first failing row in a file. The file has twelve bad rows. What does the report show?
○ All twelve rows, because the validator reports every failure.
→ A validator that stops early reports only the first, so the other eleven stay hidden.
◉ One row, and the other eleven stay hidden until the file is checked again.
→ Right. Each run finds one problem, so a person would have to fix and rerun the file twelve times.
○ Zero rows, because a validator that stops early cannot report anything.
→ It reports the first failure it finds. It just reports nothing else.
```

```quiz
A value is 2021-02-30. Which check finds the problem?
○ The shape check, because the value has the right number of digits.
→ The shape check passes this value. The problem is only visible on the calendar.
○ Neither check, because the value is text and text cannot be a date.
→ A check on the calendar is what turns text into a date or rejects it.
◉ The calendar check, which asks whether the day exists in that month.
→ Right. The form is correct, but February has no thirtieth day, so the value is not a date.
```

```quiz
A JSON record has a required email key that holds null. A second record has no email key at all. What is the right treatment?
◉ Report each separately, because a null is present with no value and a missing key is absent.
→ Right. The two reasons point to different fixes, so the message should say which one occurred.
○ Report both as the same problem, because both leave the email empty.
→ They have different causes and different fixes, so the report should keep them apart.
○ Accept both, because a null and a missing key both mean there is no email.
→ A required field fails in both cases, and the schema says so.
```

---
