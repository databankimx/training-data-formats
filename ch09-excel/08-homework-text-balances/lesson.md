# Homework: Balances Stored as Text

Read the `customers` sheet of `customers-text-numbers.xlsx` from the folder named by `TRAINING_DATA`. In this file the balances are stored as text, so the cells look like numbers but aren't. Print two lines.

1. `Text balances: ` followed by the number of balance cells that are stored as text.
2. `Text total: ` followed by the sum of those balances, read from their text and converted exactly, with exactly two decimal places.

The expected output is:

~~~text
Text balances: 12
Text total: 11311.80
~~~

Check compares your output with that, and ignores line endings and trailing spaces.

Convert each balance from its text to an exact decimal, not to a binary float. The stored texts have one, two, or no decimal places, so `4410.0` and `980.1` are both valid, and a conversion that keeps the digits as written gives the right total. Count the cells by their stored type, as the earlier sample did, and convert the text afterwards.

The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
