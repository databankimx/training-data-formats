# Homework: Total the Balances

Read `customers.json` from the folder named by `TRAINING_DATA`, and print two lines.

1. `Active customers: ` followed by the number of customers whose `active` value is `true`.
2. `Total balance: ` followed by the sum of the `balance` values of all twelve customers, with exactly two decimal places.

The expected output is:

~~~text
Active customers: 9
Total balance: 11311.80
~~~

Check compares your output with that, and ignores line endings and trailing spaces. It doesn't ignore a digit, so a total of `11311.8` or `11311.799999999999` fails.

The catch is in the second line. Floating-point numbers can't hold most decimal fractions exactly. `0.1` is stored as a value a little above one tenth, and sums of such values drift. A total that looks right on the screen can be wrong in the last digit, and a comparison with the expected output catches that. The balances here sum to a whole number of cents, so an exact method gives `11311.80` every time.

Use an exact decimal type, or work in whole cents. Python's `json` module gives you a `Decimal` if you ask it to, and C#'s `decimal` is exact for these values. In JavaScript, the safe option is to multiply each balance by 100 and round it, sum the whole numbers, then divide once at the end.

The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
