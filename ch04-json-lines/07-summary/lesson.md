# Summary: JSON Lines

This chapter covered JSON Lines: one complete value per line, read and written one line at a time, with a damaged line kept from spoiling the rest.

## What you learned

- JSON Lines is one JSON value per line, with no outer brackets and no commas between records. Each line is ordinary JSON.
- Reading is a loop over the lines. The file is never held whole, so the same code works on a file of any size.
- Writing is a loop too. Each record is serialized compactly, written as one line, and followed by a newline. A writer must escape newlines inside values, and the standard writers do.
- A line that won't parse is recorded by its number and skipped. The lines around it are unaffected, and the program keeps reading to the end.
- Only the parse error is caught. A file that can't be opened should still stop the program.
- Amounts stored as text need exact parsing, as with any money. Parse them as decimals, or work in whole cents.

## Quizzes

Three questions, one for each big idea in the chapter. Pick an answer, and read the explanation whichever way it goes.

```quiz
A JSON Lines file has a bad line in the middle. What happens to the good lines after it?
○ They are lost, because a parse error stops the file.
→ That is what happens to a JSON array. JSON Lines keeps each line independent.
◉ They are read and parsed as normal, and the bad line is reported by its number.
→ Right. Each line stands alone, so one damaged line costs only itself.
○ They are read, but only after the bad line is fixed.
→ The reader doesn't need the bad line fixed. It records the damage and moves on.
```

```quiz
A program writes a record whose note field contains a line break. What keeps the file readable?
○ Writing the note with a raw line break, so each line is still shown on its own line.
→ A raw line break inside a value would split the record across two lines, and neither half would parse.
○ Writing the note as a separate line after the record.
→ That adds a line that isn't a record, and readers will see it as damage.
◉ The writer escapes the line break as \n inside the string, so the record stays on one line.
→ Right. Standard JSON writers do this, and it's what keeps the one-record-per-line rule true.
```

```quiz
Which is the right way to read a large JSON Lines file?
◉ Read one line at a time in a loop, parsing each line as it arrives.
→ Right. Only one line is in use at any moment, so memory stays flat as the file grows.
○ Read the whole file, split it on newlines, then parse the parts.
→ That works for a small file, but it holds the whole file in memory first.
○ Wrap the file in brackets and commas, then parse it as one array.
→ That turns the file back into one value, so one bad line again stops the whole read.
```

---
