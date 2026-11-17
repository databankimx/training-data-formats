# Homework: Find the Byte-Order Mark

The file `customers-utf8-bom.csv` in the sample data folder begins with a byte-order mark. It holds the same customers as `customers.csv`, with the mark written in front of the first column name.

Write a program that reads the file and prints two lines.

1. `Starts with a byte-order mark: yes`, or `Starts with a byte-order mark: no`, depending on whether the first three bytes are `EF BB BF`.
2. `First header: ` followed by the first column name, with the byte-order mark removed. The name must match `customer_id` exactly.

Read the file from the folder named by `TRAINING_DATA`. Don't write its path into the code.

Read the bytes before you decode them. Once the file is decoded as text, the mark is a character that is easy to lose or keep without noticing, and the check is much clearer on the bytes.

The expected output is:

~~~text
Starts with a byte-order mark: yes
First header: customer_id
~~~

Check compares your output with that. It ignores line endings and trailing spaces, but it doesn't ignore a stray character in the name, so a header that still carries the mark will fail.

The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
