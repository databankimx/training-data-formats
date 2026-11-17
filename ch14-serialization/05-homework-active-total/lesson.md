# Homework: Active Total From Typed Records

Read `customers.json` from the folder named by `TRAINING_DATA`, and map each object onto a record type that declares the fields you need: `customer_id`, `active`, and `balance`. Print two lines.

1. `Active customers: ` followed by the number of customers whose `active` value is `true`.
2. `Active total: ` followed by the sum of the balances of those customers, with exactly two decimal places.

The expected output is:

~~~text
Active customers: 9
Active total: 11223.60
~~~

Check compares your output with that, and ignores line endings and trailing spaces.

The balance is a number in the file, and the total has to be exact. Declare the balance as a decimal in C# and as a `Decimal` in Python, reading it with `parse_float=Decimal` so the value never passes through a binary float. In JavaScript there is no decimal, so sum the balances in whole cents, multiplying each by 100 and rounding before the addition, and divide once at the end. The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
