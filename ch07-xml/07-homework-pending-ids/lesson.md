# Homework: Pending Order IDs

Read `orders.xml` from the folder named by `TRAINING_DATA`. Each `order` element has an `id` attribute, which is the order's identifier, and a `status` child element. Print two lines.

1. `Pending orders: ` followed by the number of orders whose `status` is `pending`.
2. `Pending ids: ` followed by the `id` attribute of each pending order, separated by a comma and a space, in the order they appear in the file.

The expected output is:

~~~text
Pending orders: 4
Pending ids: 5008, 5014, 5019, 5022
~~~

Check compares your output with that, and ignores line endings and trailing spaces.

The identifier is an attribute, not a child element, so read it with the attribute lookup, not by finding a child named `id`. A program that looks for the wrong one finds nothing, and reports zero pending orders with no error. The status is a child element, so the two come from different places in the same element.

The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
