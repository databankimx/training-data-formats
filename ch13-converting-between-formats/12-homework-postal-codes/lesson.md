# Homework: Postal Codes Through a Number

A postal code is an identifier written as digits, so it is text, and a spreadsheet or a numeric column is the usual place it is damaged. This homework shows the damage. Read `customers.csv` from the folder named by `TRAINING_DATA`, and take the postal code of each customer.

A postal code made only of digits is converted to a whole number and then back to text. Codes that contain a letter, a space, or a dash are not numbers, so they are left out of the count. Count the all-digit codes that come back different from the text they started as.

Print one line:

`Postal codes that change: ` followed by that count.

The expected output is:

~~~text
Postal codes that change: 2
~~~

Check compares your output with that, and ignores line endings and trailing spaces.

Two of the all-digit codes come back different: the ones that start with a zero. The rest come back the same, because a number written without leading zeros is the same text. Compare the text, not the number, after the round trip: a comparison of numbers would call `0155` and `155` equal, which is the very thing the chain must not do.

The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
