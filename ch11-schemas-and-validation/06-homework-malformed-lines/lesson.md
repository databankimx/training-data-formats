# Homework: Malformed Order Lines

Read `orders-lines.jsonl` from the folder named by `TRAINING_DATA`. It holds twenty-four orders, one per line. Apply two rules to each line.

1. The line must be valid JSON. If it is not, print `Line ` followed by the line number, then `: not valid JSON`, and count the line as failing.
2. The `status` field must be one of `pending`, `paid`, `shipped`, or `refunded`. If it is not, print `Line ` followed by the line number, then `: status is not allowed`, and count the line as failing.

Then print two lines:

- `Lines checked: ` followed by the number of lines.
- `Lines failing: ` followed by the number of lines with a problem.

The expected output is:

~~~text
Lines checked: 24
Lines failing: 1
Line 7: not valid JSON
~~~

Check compares your output with that, and ignores line endings and trailing spaces.

The line numbers count from one, as the earlier homework did. Line seven is cut short, so it fails the first rule and must not be checked against the second, since it has no status to read. A program that stops at the first failing line reports the wrong count. Keep reading to the end of the file, and check each line that does parse.

The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
