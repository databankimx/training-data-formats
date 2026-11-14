# Homework: Orders Per Customer

Read `orders.csv` and group the orders by `customer_id`. Count the orders in each group. Print two lines.

1. `Customers with more than one order: ` followed by the number of groups that hold two or more orders.
2. `Most orders by one customer: ` followed by the largest group count.

The expected output is:

~~~text
Customers with more than one order: 10
Most orders by one customer: 3
~~~

Check compares your output with that, and ignores line endings and trailing spaces.

Group before you count, and count the groups, not the rows. The first number is the count of groups that are large enough, and the second is the size of the largest group. A customer with a single order forms a group of one, which the first number excludes. The grouping must cover every order: the sum of the group sizes is the number of orders, which is twenty-four, and a check of that sum is a good habit before you trust either answer. The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
