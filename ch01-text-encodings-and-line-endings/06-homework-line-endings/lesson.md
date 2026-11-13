# Homework: Count the Line Endings

The file `customers-mixed-line-endings.csv` in the sample data folder has thirteen lines: a header and twelve customers. Some of its lines end in CRLF and some in LF.

Write a program that reads the file's raw bytes and prints three lines.

1. `Lines: ` followed by the number of lines. Count each line by its LF.
2. `CRLF: ` followed by the number of lines that end in CRLF.
3. `LF only: ` followed by the number of lines that end in LF alone.

Read the file from the folder named by `TRAINING_DATA`. Don't write its path into the code.

Read the bytes, not decoded text. Once the endings are translated, the difference you're counting disappears, and the count of CRLF becomes wrong.

The expected output is:

~~~text
Lines: 13
CRLF: 6
LF only: 7
~~~

Check compares your output with that, and it ignores line endings in the output itself. The numbers have to be right.

Think about what a CRLF is in bytes before you write the count. Two bytes make one ending, so a count of LF bytes gives the number of lines, and the bytes before each LF tell you which kind it is.

The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
