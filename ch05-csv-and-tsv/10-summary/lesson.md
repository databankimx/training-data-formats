# Summary: CSV and TSV

This chapter covered CSV and TSV: a grid of text whose structure depends entirely on the quoting rules.

## What you learned

- A CSV record is usually a line, with fields separated by the delimiter. A field containing the delimiter, a quote, or a line break must be quoted, and a quote inside a quoted field is doubled.
- A quoted field can hold a line break, so the number of lines is not the number of records.
- Splitting each line on commas is wrong as soon as a value contains a comma. A quote-aware reader follows the switch between quoted and unquoted text.
- A correct writer quotes only the fields that need it, and doubles any quote inside them. Joining strings by hand is where the errors come from.
- A row whose field count differs from the header is damage. Report it by line number rather than guessing which field is missing.
- A text field that starts with `=`, `+`, `-`, or `@` may be a formula when the file is opened in a spreadsheet. Report it, and decide what to do with it in the program that owns the data.
- TSV uses the same rules with a tab as the delimiter. A comma needs no quotes in TSV, and a tab is the value that's hard to represent.

## Quizzes

Three questions, one for each big idea in the chapter. Pick an answer, and read the explanation whichever way it goes.

```quiz
A CSV file has a name field written as "Okafor, Chidi". A reader splits each line on commas. What happens?
○ The record is rejected, because the file is invalid.
→ The file is valid. The problem is in the reader, which doesn't follow the quoting rules.
◉ The name splits in two, and every later value moves one column to the right.
→ Right. The split doesn't stop at the quoted comma, so the columns after it shift without any error.
○ The name is read correctly, because a comma inside a name is always fine.
→ A comma is ordinary text only inside quotes. A splitter that ignores quotes treats it as a separator.
```

```quiz
A CSV file has 12 records, and a line count of 14. How is that possible?
◉ One record has a quoted field that holds a line break, so one record spans two lines.
→ Right. A line break inside quotes doesn't end the record, so the line count and the record count differ.
○ The file has two damaged records, and the line count is correct.
→ A ragged row doesn't add a line. The extra lines come from somewhere else.
○ The file has two blank lines at the end, which the reader should have ignored.
→ Blank lines would count, but the explanation is the quoted line break, which is what the sample shows.
```

```quiz
A row has 10 fields when the header has 11. What should a reader do?
○ Pad the row with an empty field at the end, so the counts match.
→ That guesses which field is missing, and the guess may put values in the wrong columns.
○ Stop reading the file, because the file is damaged.
→ Stopping throws away the good rows. Reporting the row is the safer choice.
◉ Report the row by its line number, and let someone decide what it means.
→ Right. The reader can't know which field is missing, so it reports the damage and leaves the decision to a person.
```

---
