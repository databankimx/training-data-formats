# Homework: Norwegian Customers

Read `customers.yaml` from the folder named by `TRAINING_DATA`. Count the customers whose `country_code` is `NO`, and print one line:

`Norwegian customers: ` followed by the count.

The expected output is:

~~~text
Norwegian customers: 1
~~~

Check compares your output with that, and ignores line endings and trailing spaces.

The code `NO` is a country, and the file holds it as a quoted string. The count is only correct if the code stays text. A program that reads the value as a boolean would compare `False` with `NO`, find no match, and report zero, which is the Norway problem in a homework answer. Read the value as text, and compare it as text.

The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
