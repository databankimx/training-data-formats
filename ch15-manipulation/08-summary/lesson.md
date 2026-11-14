# Summary: Manipulation

This chapter covered the work done on rows once they are loaded: filtering, renaming, computing, grouping, and joining.

## What you learned

- A filter keeps the rows that match a condition, and its total should be checked against an independent figure.
- A rename changes names, not values. A rename applied to one table and not the other breaks a join without an error.
- A computed value is exact only with an exact type. A float multiplied by one hundred can miss a whole cent.
- A grouping collects rows by key, and the sum of the group counts must equal the number of rows. A key with stray spaces forms a group of its own.
- A join's left side decides which rows appear. A left join keeps customers with no orders, and an inner join drops them.
- A count of distinct keys and a total of amounts answer different questions. Keep the two groupings apart.

## Quizzes

Three questions, one for each big idea in the chapter. Pick an answer, and read the explanation whichever way it goes.

```quiz
A join is started from the orders, and a customer with no orders is absent from the result. What is the right way to find such customers?
○ Count the orders for each customer, because a customer with no orders will show a count of one.
→ A customer with no orders does not appear in the orders at all, so no count can show it.
◉ Start the join from the customers, so that every customer is kept, and count those with no matching orders.
→ Right. The left side of the join decides which rows survive, so the customers are the side to start from.
○ Use an inner join, because it keeps every row that has a match and so finds the missing customers.
→ An inner join drops the rows without a match. It is the join that hides the customers with no orders.
```

```quiz
The grouping by status gives counts that add to 23, but the file has 24 rows. What is the most likely cause?
○ The file has a duplicate row, which the grouping removed.
→ A grouping does not remove rows. Each row is counted in exactly one group.
○ The counts are right, because a total of 23 is a correct count of paid orders.
→ The total is of all the orders, and the count of 23 means a row went missing.
◉ One row has a status that differs by a space or a capital letter, so it formed a group the list did not show.
→ Right. A group nobody listed holds the missing row, and the total exposes it.
```

```quiz
A computed balance in cents is taken from a float multiplied by one hundred, then truncated. What can go wrong?
◉ A product that should be a whole number of cents can come out one cent short, because the truncation drops the fraction.
→ Right. Rounding before the conversion, or an exact type, avoids the loss.
○ Nothing, because a float keeps every cent exactly.
→ A float holds many decimals only approximately, and the multiplication can be just under a whole number.
○ The result is always too large, because a float rounds up.
→ A float can round either way, so the error can go in either direction.
```

---
