# Homework: Shipped Customers

Read `orders.csv` and keep the orders whose `status` is `shipped`. Count the distinct customers who have at least one shipped order, and total the amounts of all the shipped orders. The count is of customers, not orders: a customer with two shipped orders counts once. Print two lines.

1. `Customers with a shipped order: ` followed by the number of distinct `customer_id` values among the shipped orders.
2. `Shipped total: ` followed by the sum of the shipped amounts, with exactly two decimal places.

The expected output is:

~~~text
Customers with a shipped order: 7
Shipped total: 3649.03
~~~

Check compares your output with that, and ignores line endings and trailing spaces.

The count and the total answer different questions, and they use different groupings. A set of customer ids gives the count, and it ignores repeats. The total is over orders, so each order's amount is added once, even when a customer has two of them. Keep the two apart in your code, so one does not change the other. The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
