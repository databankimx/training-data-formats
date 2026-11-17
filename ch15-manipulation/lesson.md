# 15. Manipulation

Manipulation is the work done on rows once they are loaded: keeping some of them, renaming fields, computing new values, grouping rows that share a key, and joining one table to another. Most of a data task is a combination of these, and most of the mistakes are in the details: a join that drops customers with no orders, a grouping that counts the wrong thing, a computed total that loses its exactness, or a filter that treats an empty value as a match.

This chapter works with the two good tables from the sample data: `customers.csv`, with the twelve customers, and `orders.csv`, with twenty-four orders that each refer to a customer by `customer_id`. Every operation is shown on those two tables, so the results can be checked against the same dataset the earlier chapters used.

The samples read the files through TRAINING_DATA and parse them with the libraries already declared for CSV in the earlier chapters. The operations themselves are written out in each sample, so the filter, the group, and the join are visible in the code.

**Libraries.** No new libraries. C# uses CsvHelper 33.1.0 for reading, along with `System.Linq` and `System.Globalization`. Python uses the standard `csv`, `collections`, `decimal`, and `os` modules. JavaScript uses `csv-parse`, already pinned in `samples\package.json`, along with `node:fs` and `node:path`.

The chapter has a reading step, four samples, two homework items, and a summary with three quizzes.

---
