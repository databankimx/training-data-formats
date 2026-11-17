# What Manipulation Is

Five manipulations cover most of the work. A filter keeps the rows that meet a condition, and drops the rest. A rename changes the name of a column, and nothing else. A computation adds a value derived from others, such as a balance in cents. A grouping collects the rows that share a key, so that each group can be counted or totalled. A join combines two tables by matching a key in each.

Each one changes the data in a different way, and each has its own way of going wrong. A filter that compares an empty value to a text keeps the row or drops it by accident, depending on the language. A rename that is applied to one table and not the other breaks a join with no error. A computation that uses floats gives a total that is close and not exact. A grouping that is keyed on text with a trailing space creates two groups for one customer.

A join needs the most care, because it's where rows disappear. An inner join keeps only the rows that match on both sides, so a customer with no orders is absent from the result without a warning. A left join keeps every row of the left table and fills the right side with nothing for a row with no match. The choice decides what the result means, and the count of rows is the first check: a join that returns fewer rows than the left table has either dropped rows on purpose or lost them by mistake.

Every manipulation should be checked against an independent count or total, computed another way. The samples in this chapter do that: the paid total in the filter sample is the same figure the JSON Lines chapter produced from the same orders, and the grouping counts add back up to the number of orders.

> **Aside: a manipulation is a claim about the rows.**
> A filter says these rows matter, and a group says these rows belong together. Each is a decision that a reader of the output will trust, so write the condition in the code where it can be read.

> **Common mistake.** Joining on a key that has different text on the two sides, such as `1001` in one table and ` 1001` with a space in the other. The join matches nothing for that customer, and the inner join drops the customer silently. Clean the key first, as Chapter 12 showed.

---
