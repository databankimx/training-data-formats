# Homework: Duplicate Customer IDs

Read `customers-duplicates.csv` from the folder named by `TRAINING_DATA`. The file has a header row and fourteen data rows. The schema requires `customer_id` to be unique, and two identifiers are repeated later in the file. Print the report.

1. For each row whose `customer_id` has already appeared on an earlier row, print `Line ` followed by the line number, then `: customer_id ` followed by the identifier, then ` is a duplicate`. The header is line one.
2. `Rows checked: ` followed by the number of data rows.
3. `Rows failing: ` followed by the number of rows with a problem.

The expected output is:

~~~text
Rows checked: 14
Rows failing: 2
Line 14: customer_id 1003 is a duplicate
Line 15: customer_id 1007 is a duplicate
~~~

Check compares your output with that, and ignores line endings and trailing spaces.

The first occurrence of each identifier is valid, and only the later one is reported. The duplicate on line 14 has a different balance from the original, and that difference is not part of this rule, so the row fails only on its identifier. Remember to print the report lines before the two counts, as in the expected output. A set of identifiers already seen is the simplest way to track repeats in one pass.

The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
