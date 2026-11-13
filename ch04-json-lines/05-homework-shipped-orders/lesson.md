# Homework: Shipped Orders

Read `orders-lines.jsonl` from the folder named by `TRAINING_DATA`, one line at a time. Print two lines.

1. `Shipped orders: ` followed by the number of orders whose `status` is `shipped`.
2. `Skipped lines: ` followed by the number of lines that could not be parsed.

The expected output is:

~~~text
Shipped orders: 7
Skipped lines: 1
~~~

Check compares your output with that, and ignores line endings and trailing spaces.

The file has eight orders marked shipped, but one of them is the damaged line, which can't be parsed. The count of shipped orders counts only the lines that parse, and the damaged line counts as skipped. Read the whole file: a program that stops at the first bad line will report fewer skipped lines and a different shipped total.

The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
