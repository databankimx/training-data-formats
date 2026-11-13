# Homework: Active Total, Skipping Short Lines

Read `customers-fixed-short-row.fixed` from the folder named by `TRAINING_DATA`. It has the same layout as `customers.fixed`, but one line is too short to hold every field, and that line must be skipped rather than read. Print three lines.

1. `Active customers counted: ` followed by the number of active customers on lines that have every field.
2. `Active total: ` followed by the sum of the balances of those active customers, with exactly two decimal places.
3. `Skipped short lines: ` followed by the number of lines that are too short to read.

The expected output is:

~~~text
Active customers counted: 8
Active total: 10243.50
Skipped short lines: 1
~~~

Check compares your output with that, and ignores line endings and trailing spaces.

Two things to get right. A line shorter than 56 characters must be counted and skipped before you cut any field from it, or the reading may fail or return a partial value. And the total must be exact. Parse each balance as a decimal, as in the earlier homework, or work in whole cents, so the sum has no float error.

The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
