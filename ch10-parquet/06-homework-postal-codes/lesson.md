# Homework: Postal Codes Starting with 0

Read `customers.parquet` from the folder named by `TRAINING_DATA`. Each customer has an `address` struct, and its `postal_code` field is a string. Print one line:

`Postal codes starting with 0: ` followed by the number of customers whose `address.postal_code` begins with the digit 0.

The expected output is:

~~~text
Postal codes starting with 0: 2
~~~

Check compares your output with that, and ignores line endings and trailing spaces.

The postal code is text, and some of them begin with a zero: `0155` in Oslo and `00100` in Nairobi. A program that converts the column to a number would lose those leading zeros, and then no code would start with 0 at all. Read the field as a string, and test the first character. The field is inside the struct, so the lookup goes through `address` first.

The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
