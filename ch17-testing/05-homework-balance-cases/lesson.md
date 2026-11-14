# Homework: Balance Cases

Write a function named `toCents` (or `ToCents` in C#, `to_cents` in Python) that takes a balance's text and returns its value in whole cents, exactly. The text has no more than two decimal places, and it may have none. The function must not pass the text through a binary float.

Check it against four fixed cases, which are typed into the code:

| Input | Expected cents |
|---|---|
| `1250.75` | 125075 |
| `0.00` | 0 |
| `980.1` | 98010 |
| `4410` | 441000 |

For each case, count a pass when the function returns the expected value, and a failure when it does not. Print two lines and nothing else:

1. `Cases passed: ` followed by the number of passes.
2. `Cases failed: ` followed by the number of failures.

The expected output is:

~~~text
Cases passed: 4
Cases failed: 0
~~~

Check compares your output with that, and ignores line endings and trailing spaces.

Write the function first, then the checks. The text `980.1` has one decimal place, so the function must pad it to two places, not read it as `980` with a stray digit. Do the conversion on the text, splitting at the decimal point, or use an exact decimal type. The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
