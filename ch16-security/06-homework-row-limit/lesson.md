# Homework: Row Limit

Read `customers.csv` from the folder named by `TRAINING_DATA`. The file has a header row and twelve data rows. The program will accept at most ten data rows, and it refuses the rest without parsing them. Print two lines.

1. `Rows accepted: ` followed by the number of data rows accepted, at most ten.
2. `Rows refused: ` followed by the number of data rows beyond the limit.

The expected output is:

~~~text
Rows accepted: 10
Rows refused: 2
~~~

Check compares your output with that, and ignores line endings and trailing spaces.

Stop parsing when the limit is reached, as the streamed sample did. The refused rows are counted by reading their lines without parsing them, since counting a line costs far less than parsing it and keeping it. The header is not counted, and the limit is measured against data rows only. Do not build a list of the rows beyond the limit, because that would hold the untrusted content in memory. The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
