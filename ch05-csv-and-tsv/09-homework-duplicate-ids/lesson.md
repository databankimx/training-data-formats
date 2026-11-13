# Homework: Duplicate IDs

Read `customers-duplicates.csv` from the folder named by `TRAINING_DATA`. The file has a header row and then fourteen records. Two of the customers appear twice: one repeat has a changed balance, and the other is an exact copy. Print three lines.

1. `Rows: ` followed by the number of data rows, not counting the header.
2. `Unique customer ids: ` followed by the number of different `customer_id` values.
3. `Repeated ids: ` followed by the repeated identifiers, separated by a comma and a space. List each one in the order it first appears as a repeat, not in numeric order.

The expected output is:

~~~text
Rows: 14
Unique customer ids: 12
Repeated ids: 1003, 1007
~~~

Check compares your output with that, and ignores line endings and trailing spaces.

The repeats are the rows at the end of the file. A program that keeps a record of the identifiers it has seen can report a repeat as soon as it finds one. Then the first repeat is 1003, because it appears twice before 1007 does. Reporting the identifiers in sorted order would put 1003 and 1007 in the same order here, but the order of first repeat is the rule the expected output follows.

The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
