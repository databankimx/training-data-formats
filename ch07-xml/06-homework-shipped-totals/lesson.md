# Homework: Shipped Totals

Read `orders.xml` from the folder named by `TRAINING_DATA`. The root element holds twenty-four `order` elements. Each order has an `id` attribute, and child elements `customer_id`, `order_date`, `amount`, and `status`. Print two lines.

1. `Shipped orders: ` followed by the number of orders whose `status` is `shipped`.
2. `Shipped total: ` followed by the sum of the `amount` values of those orders, with exactly two decimal places.

The expected output is:

~~~text
Shipped orders: 8
Shipped total: 3649.03
~~~

Check compares your output with that, and ignores line endings and trailing spaces.

Two things to get right. The parser must refuse or ignore external references, as the samples showed, even though this file has none, so the habit carries over to the files you will meet. And the amounts are text in the element, so parse them as exact decimals, or sum whole cents, as in the money homework of the earlier chapters.

The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
