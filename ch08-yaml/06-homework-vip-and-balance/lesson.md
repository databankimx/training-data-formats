# Homework: VIP Count and Balance Total

Read `customers.yaml` from the folder named by `TRAINING_DATA`. The file is a list of twelve customers. Each has a `tags` list, and a `balance` that is quoted, so it reads as text. Print two lines.

1. `VIP customers: ` followed by the number of customers whose `tags` list contains `vip`.
2. `Total balance: ` followed by the sum of the `balance` values of all twelve customers, with exactly two decimal places.

The expected output is:

~~~text
VIP customers: 3
Total balance: 11311.80
~~~

Check compares your output with that, and ignores line endings and trailing spaces.

The balance is text, so convert it with an exact decimal type, or work in whole cents, as in the money homework of the earlier chapters. The tags are a real list, so test membership in the list rather than searching the text for the word `vip`, which would also match a tag such as `vip-lapsed` if one existed.

The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
