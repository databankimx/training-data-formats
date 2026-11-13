# Homework: Largest Balance and Active Count

Read `customers.fixed` from the folder named by `TRAINING_DATA`. The layout is in the first step: the balance is at positions 40 to 47, and the active flag is at positions 49 to 53. Print two lines.

1. `Active customers: ` followed by the number of lines whose active flag is `true`.
2. `Largest balance: ` followed by the largest balance, written exactly as it appears in the file.

The expected output is:

~~~text
Active customers: 9
Largest balance: 4410.00
~~~

Check compares your output with that, and ignores line endings and trailing spaces. It doesn't ignore a digit, so `4410` or `4410.0` fails, even though they're the same number.

Two things to get right. Cut each field by its position and trim it, as the reading sample did, and compare the flag as text, which is `true` or `false`. For the largest balance, compare the values as numbers, but print the field's own text, so the two decimal places in the file survive. A program that converts `4410.00` to a float and prints it gets `4410`, which is the wrong output here.

The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
