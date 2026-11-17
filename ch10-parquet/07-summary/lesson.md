# Summary: Parquet

This chapter covered Parquet: a columnar file with its schema in the footer, whose types travel with the data.

## What you learned

- A Parquet file stores each column together, in row groups, and the schema and statistics sit in the footer at the end.
- A reader can skip the columns it doesn't need, and a truncated file without its footer can't be read.
- Physical types are few, and logical types such as decimals, strings, lists, and structs say what the values mean.
- A decimal is stored as an exact scaled integer, so a balance keeps its two places through reading and writing.
- A struct and a list are read as nested values. An empty list is a value, not a null, so test its length.
- A string column keeps its leading zeros. Converting a postal code to a number loses them.
- A writer keeps the type you give it. A balance written as a double is only as exact as a binary float.

## Quizzes

Three questions, one for each big idea in the chapter. Pick an answer, and read the explanation whichever way it goes.

```quiz
A program wants only the balance column from a wide Parquet file. What does the format let it do?
○ Read the whole file and then discard the other columns.
→ Parquet can avoid that work, because each column is stored separately.
◉ Read only the chunks for the balance column and skip the rest.
→ Right. The footer says where each column's data is, so the other columns are never read.
○ Convert the file to CSV first, so that it can read one column at a time.
→ That conversion reads everything once, and it throws away the types the format keeps.
```

```quiz
A customer has an empty tags list. Which test correctly finds customers with no tags?
◉ The length of the tags list is zero.
→ Right. The list exists and holds nothing, so its length is the test.
○ The tags value is None, which is how an empty list appears.
→ An empty list is not a null, so this test is false for every customer.
○ The tags value is missing from the row.
→ The column is present for every row. The list is simply empty.
```

```quiz
A postal code column holds 0155 for an address in Oslo. What happens if the column is converted to a number?
○ The code stays 0155, because a number keeps its digits.
→ A numeric value does not keep the zeros it was written with.
○ The conversion fails with an error, so the value is never read.
→ The conversion succeeds silently, which is why the loss is easy to miss.
◉ The leading zero is lost, and the code becomes 155.
→ Right. A number has no leading zeros, so the text no longer matches the stored value.
```

---
