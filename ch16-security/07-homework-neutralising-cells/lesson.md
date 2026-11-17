# Homework: Neutralising Cells

The four values below are typed into the code, so the data is inline. Each one is a cell from a file someone else sent.

- `=1+1`
- `Alice`
- `-45.00`
- `@SUM(A1)`

Apply the neutralising rule from the sample to each value. A value that starts with `=`, `+`, `-`, or `@` is neutralised unless it is a plain number. Print two lines and nothing else:

1. `Neutralised: ` followed by the number of values the rule changes.
2. `Left alone: ` followed by the number of values the rule leaves unchanged.

The expected output is:

~~~text
Neutralised: 2
Left alone: 2
~~~

Check compares your output with that, and ignores line endings and trailing spaces.

Two of the values start with a formula character and are not numbers, so they are neutralised. The third starts with a minus sign and is a number, so it is left alone. The fourth has no formula character, and it is also left alone. Do not print the values: the counts are the answer, and a value printed into the log is the mistake the logging sample described. The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
