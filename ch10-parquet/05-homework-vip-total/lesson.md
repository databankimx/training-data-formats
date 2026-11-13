# Homework: VIP Count and Exact Total

Read `customers.parquet` from the folder named by `TRAINING_DATA`. It has twelve rows, with a `tags` list and a `balance` decimal. Print two lines.

1. `VIP customers: ` followed by the number of customers whose `tags` list contains `vip`.
2. `Total balance: ` followed by the sum of the `balance` values of all twelve customers, with exactly two decimal places.

The expected output is:

~~~text
VIP customers: 3
Total balance: 11311.80
~~~

Check compares your output with that, and ignores line endings and trailing spaces.

The balances are decimals in the file, so keep them as decimals. Converting each one to a float, or to an integer by dropping the point, changes the total in some languages. The tags are a list, so test membership in it, not in a joined string, because a joined string would also match a tag that contains `vip` as part of a longer word.

The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
