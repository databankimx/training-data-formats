# What JSON Lines Is

A JSON array is one value. It starts with a bracket and ends with a bracket, and everything in between belongs to it. A parser has to read the whole thing before it can say anything about the first record, and one error anywhere makes the whole file unreadable. `customers.json` is an example of that shape.

JSON Lines, also written as NDJSON, is a different arrangement. Each line of the file is a complete JSON value, usually an object, and the lines are separated by a newline character. There's no outer bracket and no commas between records. `customers.jsonl` has twelve lines, and each one parses by itself.

That independence has three practical consequences. A program can read the file one line at a time, so it never holds the whole file in memory. A writer can append a record without rewriting the file. And a bad line can be reported and skipped, because the lines around it don't depend on it. The last of these is the one this chapter's samples test.

The format has a few rules that matter. A JSON writer must never put a newline inside a value, and every standard writer escapes newlines inside strings, so the rule holds for normal output. A file ends with a newline, and an empty last line is not a record. Some tools write CRLF line endings, and a reader has to remove the carriage return before it parses the line, as Chapter 1 showed.

> **Aside: JSON Lines is not a different JSON.**
> Each line is ordinary JSON, so every rule from the last chapter applies to it: the same six value types, the same number problems, the same null and missing-key distinction. The format only changes how the records are laid out in the file.

> **Common mistake.** Reading a JSON Lines file as one JSON array by wrapping it in brackets and adding commas. It works until a line has a trailing comma or a stray newline inside a string, and then the wrap hides the real error. Read the file one line at a time.

---
