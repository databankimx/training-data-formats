# Homework: VIP Customers and Their Cities

Read `customers.json` from the folder named by `TRAINING_DATA`. Some customers have the tag `vip` in their `tags` list. For each customer with that tag, print one line: the customer's `customer_id`, a space, then the city from the nested `address` object.

Print the customers in the order they appear in the file. The expected output is:

~~~text
1001 Springfield
1004 Oslo
1008 Galway
~~~

Check compares your output with that, and ignores line endings and trailing spaces.

Three things to get right. The tag test is on the list, not on the whole `tags` value: a customer whose tags are `["newsletter"]` isn't a VIP, and a customer whose tags are `[]` has none. The city is inside `address`, so it's `address.city`, not a top-level key. And the identifier should print as a whole number, with no decimal point, which is simpler here than in the large-integers sample.

The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
