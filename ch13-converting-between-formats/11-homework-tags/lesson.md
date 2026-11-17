# Homework: Tags After a Conversion

Every link in the chain stores the tags as one text value, such as `vip;newsletter`. A list has been joined into text, and the joining is a change in form. This homework reads the tags back into a list and counts them.

Read `customers.csv` from the folder named by `TRAINING_DATA`. Split each `tags` value on the semicolon, and drop the empty items. Print two lines.

1. `Tags in the list: ` followed by the total number of tags across all customers.
2. `Customers with no tags: ` followed by the number of customers whose list is empty.

The expected output is:

~~~text
Tags in the list: 12
Customers with no tags: 2
~~~

Check compares your output with that, and ignores line endings and trailing spaces.

Two traps are waiting. Splitting an empty value on the semicolon gives one empty item, so a customer with no tags would count as having one tag. Dropping the empty items fixes that. And counting the customers with no tags should look at the list after the empties are dropped, not at the text, because the text of an empty list is an empty string and the same test on the text gives the same answer only by accident.

The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
