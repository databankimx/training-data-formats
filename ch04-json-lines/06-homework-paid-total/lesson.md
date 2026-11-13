# Homework: Paid Total

Read `orders-lines.jsonl` from the folder named by `TRAINING_DATA`, one line at a time. The `amount` of each order is stored as text, such as `"45.00"`, not as a number. Print two lines.

1. `Paid orders: ` followed by the number of orders whose `status` is `paid`.
2. `Paid total: ` followed by the sum of the `amount` values of those orders, with exactly two decimal places.

The expected output is:

~~~text
Paid orders: 9
Paid total: 4103.45
~~~

Check compares your output with that, and ignores line endings and trailing spaces.

Two things to get right. The damaged line must be skipped, not counted, and the sum must be exact. Parse each amount as a decimal, not as a binary float, so that the total has no drift. The Chapter 3 homework showed the same trap with balances. Here the amounts are text, so the parse is yours to choose: a decimal type in C# and Python, and whole cents in JavaScript.

The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
