# Summary: Security With Untrusted Input

This chapter covered the ways a file can harm the program that reads it, and the defences that follow one rule: decide what the input may be before the program acts on it.

## What you learned

- A file can harm a program by its size, its structure, its references, its formulas, and its effect on the log.
- A size limit is checked on the file's metadata before the file is read. A limit checked after parsing protects nothing.
- A formula cell is neutralised with an apostrophe, unless it is a plain number, since a negative amount is legitimate.
- A stream is limited by the number of lines it may read, and the reader reports that it stopped.
- A log entry gives the location, the field, and the reason, and not the untrusted value.
- Exponential entity expansion and archive expansion are defended by limits on depth and on expanded size, not by generating examples of the attack.

## Quizzes

Three questions, one for each big idea in the chapter. Pick an answer, and read the explanation whichever way it goes.

```quiz
A program reads a file fully, counts its records, and then refuses it because it has too many. What is wrong with that design?
○ Nothing, because the count is accurate and the refusal is correct.
→ The count is accurate, but the memory is already spent. The limit protects nothing once the work is done.
◉ The limit comes after the work, so the defence does not stop the memory or the time being used.
→ Right. A limit must be checked before the expansion, on the file's size or as the data is read.
○ The program should refuse the file on its name alone, because a name shows the size.
→ A name says nothing reliable about size. The check must be on the file itself.
```

```quiz
A log line for a bad value contains the value itself, and the value includes a line break followed by text. What can happen?
○ Nothing, because a log line always holds exactly one value.
→ A log writer adds a line break for each entry, and the input can add its own.
○ The log is only at risk if it is printed to a terminal.
→ The false entry is in the file itself, and any reader of the log can be misled by it.
◉ The input can write a second, false log entry, because its line break starts a new line in the log.
→ Right. Logging the location and the reason, and not the value, keeps the input from shaping the log.
```

```quiz
A cell that begins with a minus sign holds the number -45.00. Should the formula rule neutralise it?
◉ No, because it is a plain number, and an apostrophe would turn a legitimate amount into text.
→ Right. The rule covers formulas, and a number is not a formula, so it is left alone.
○ Yes, because every value that begins with a formula character is a formula.
→ A negative amount begins with the same character, and the rule must allow for it.
○ Yes, because a minus sign at the start always means a formula.
→ A minus sign at the start of a number is a sign, not a formula.
```

---
