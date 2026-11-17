# Homework: Active Total from a Workbook

Read the `customers` sheet of `customers.xlsx` from the folder named by `TRAINING_DATA`. The sheet has a header row and twelve customers. Print two lines.

1. `Active customers: ` followed by the number of customers whose `active` cell is `TRUE`.
2. `Total balance: ` followed by the sum of the `balance` cells of all twelve customers, with exactly two decimal places.

The expected output is:

~~~text
Active customers: 9
Total balance: 11311.80
~~~

Check compares your output with that, and ignores line endings and trailing spaces.

The balances are numbers stored in the file, so read them as numbers, not as the text the screen shows. A balance such as `980.1` is stored as a number that displays as `980.1`, and a program should not add the display's decimal places to it. Convert each number to exact decimal cents before you add, so the total has no floating-point drift. The sheet's first row is the header, so start the count one row down.

The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
