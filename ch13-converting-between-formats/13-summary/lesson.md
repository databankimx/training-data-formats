# Summary: Converting Between Formats

This chapter took the customer data through a loop of nine formats, and back to the start. Each link read the output of the one before it, and the last link compared the result with the original.

## What you learned

- Every fact in a conversion is kept, changed in form, or lost. A safe conversion has no loss that goes unrecorded.
- A list is changed in form when it's joined into text, and it has to be split again on the way back. An empty list is not the same as a list with one empty item.
- A nested object is kept by JSON, XML, YAML, and Parquet, and flattened into columns by CSV, TSV, fixed-width, and Excel.
- A balance is kept exactly only where the format stores decimals. Written as a binary float, or as a bare number that is later read as one, it loses its exact value.
- A balance written as a number loses its text. `0.00` becomes `0`, and the value is the same. Writing it again with two decimal places restores the text.
- A postal code is text. A number has no leading zeros, so converting `0155` to a number and back gives `155`.
- A loop tests every link at once, but a check on values alone cannot see a change of text. The final comparison must check both.

## Quizzes

Three questions, one for each big idea in the chapter. Pick an answer, and read the explanation whichever way it goes.

```quiz
A balance of 0.00 is written to Excel as a number and read back as 0. What has changed?
○ The value has changed, because zero and 0.00 are different numbers.
→ They are the same number. Only the text differs.
◉ The text has changed, but the value is the same, so a value-only check would pass.
→ Right. A comparison of values misses this, which is why the chain checks both.
○ Nothing has changed, because a spreadsheet stores the same digits.
→ The text changed from two decimal places to none, and a text comparison would show it.
```

```quiz
A postal code 0155 is converted to a number and back to text. What is the result?
○ 0155, because the text is kept whenever it is converted.
→ A conversion to a number does not keep the text. The zero is lost unless the text is kept separately.
○ An error, because a postal code cannot be a number.
→ A digit-only postal code converts without error, and the loss is silent.
◉ 155, because a number has no leading zeros.
→ Right. The text comes back different, so the postal code is changed in form and lost.
```

```quiz
A list of tags is joined into one text value, such as vip;newsletter. What must the next link do with an empty value?
◉ Read it as an empty list, dropping the empty items after the split.
→ Right. A customer with no tags has no tags, and the list should say so.
○ Read it as one tag containing an empty string, because that is what a split returns.
→ A split returns one empty item for an empty value, which is wrong for a list of tags.
○ Reject the record, because an empty tags value is invalid.
→ An empty list is a valid value, and rejecting the record would discard good data.
```

---
