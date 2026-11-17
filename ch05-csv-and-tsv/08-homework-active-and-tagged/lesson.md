# Homework: Active and Tagged

Read `customers.csv` from the folder named by `TRAINING_DATA`. The file has a header row, then twelve records. Print two lines.

1. `Active customers: ` followed by the number of records whose `active` field is `true`.
2. `Tagged customers: ` followed by the number of records whose `tags` field is not empty. The tags are separated by semicolons, and an empty field means no tags.

The expected output is:

~~~text
Active customers: 9
Tagged customers: 10
~~~

Check compares your output with that, and ignores line endings and trailing spaces.

Two things to get right. The second customer's name is quoted and contains a comma, so the parser must read it as one field, or every column after it shifts and the counts go wrong. The `active` and `tags` fields are text: compare `true` as a string, and check the tags field for length, not for a list of values. You don't need to split the tags to count customers who have any.

The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
