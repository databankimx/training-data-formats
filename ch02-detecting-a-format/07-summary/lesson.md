# Summary: Detecting a Format

This chapter taught detection by content. A file's name is a label, and a detector reads the first bytes to find the kind of file it really is.

## What you learned

- A file's extension is a label that nothing checks. The content is the reliable test.
- Each format starts with a signature: Parquet begins with `PAR1`, a zip archive begins with `PK` and the bytes `03 04`, XML begins with `<?xml`, and JSON begins with `[` or `{` after any whitespace.
- Modern Excel workbooks, `.xlsx`, are OpenXML files, which are zip archives of XML files, so a detector reports them as zip. Legacy `.xls` workbooks use the OLE2 signature instead, `D0 CF 11 E0 A1 B1 1A E1`.
- The checks run in order, from the most specific signature to the broadest. Text is the last check, because JSON is text too.
- Detection tells you the kind of file, not whether it is well formed. A truncated JSON file is still JSON.
- A byte-order mark doesn't change the kind of a file. A text file can start with one.

## Quizzes

Three questions, one for each big idea in the chapter. Pick an answer, and read the explanation whichever way it goes.

```quiz
A file is named customers.csv, and its first byte is a bracket, [. What does a detector conclude?
○ That the file is CSV, because the name says so.
→ The name is a label. The content is the reliable test, and the content begins with a bracket.
○ That the file is text, because a bracket is a printable character.
→ Text is the last check. A bracket is caught earlier, by the JSON signature.
◉ That the file is JSON, whatever its name says.
→ Right. The JSON check matches the bracket, before the broad text rule can apply.
```

```quiz
A detector reads a file whose first four bytes are PK and then 03 04. What kind does it report?
◉ A zip archive, which may be an Excel workbook.
→ Right. The zip signature says zip. Whether the archive is a workbook needs a look inside.
○ An Excel workbook, because Excel files are common.
→ Excel workbooks are zip archives, so the signature says zip. The workbook question needs more.
○ Binary, because the bytes are not text.
→ A zip archive has a signature, so it is matched before the binary rule applies.
```

```quiz
A JSON file has been cut off halfway through. What does a detector report?
○ Binary, because the file is damaged.
→ Detection looks at the kind, not the validity. The start is intact, so the kind is still JSON.
○ Text, because a damaged file can't be trusted.
→ Detection doesn't judge validity. The start of the file still matches the JSON signature.
◉ JSON, because the start of the file is intact.
→ Right. The detector reports the kind. A parser that reads the whole file is what finds the truncation.
```

---
