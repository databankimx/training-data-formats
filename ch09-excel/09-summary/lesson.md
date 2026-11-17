# Summary: Excel

This chapter covered workbooks: their parts, the types their cells store, and the checks a program needs before it trusts a value.

## What you learned

- An `.xlsx` file is a zip of XML parts. The libraries read those parts, and a program asks only for sheets and cells.
- A cell stores a type: text, number, boolean, error, or formula. The type is what decides whether arithmetic works.
- The display format is not the stored value. A balance can show two decimal places and hold a number with fewer.
- A number stored as text looks almost identical to a number. Check the stored type, then convert the text exactly.
- A formula cell holds an expression and its last result. Scan for formulas in a workbook from outside before it is opened in Excel.
- The legacy `.xls` format is binary, and only some libraries read it. Python's `xlrd` does, and the xlsx libraries here do not.
- A library returns the stored value, not the displayed one. Read the cell, and never the formatted text.

## Quizzes

Three questions, one for each big idea in the chapter. Pick an answer, and read the explanation whichever way it goes.

```quiz
A balance cell shows 980.10 in Excel. What value does a program read from it?
○ The text 980.10, because the display shows that text.
→ The display is a format applied to the value. The program reads the stored number.
◉ The number 980.1, because the stored value has no trailing zeros.
→ Right. The format adds the second decimal place on screen, but the stored number is 980.1.
○ The number 980.1 with a flag saying it was formatted.
→ Excel doesn't record the format in the value. The format is separate, in the styles part.
```

```quiz
A column of balances shows a small green triangle in each cell. What does that mean?
○ The values are the correct numbers, and the triangle marks a total.
→ A total would appear in a separate row, not as a triangle in each cell.
◉ The values are stored as text, so a sum over them would ignore them or give the wrong result.
→ Right. The triangle is Excel's warning that the cell looks like a number but is stored as text.
○ The cells contain formulas, and each one is calculating its value.
→ Formula cells don't carry the triangle. The triangle marks text that looks like a number.
```

```quiz
A workbook from outside your system is opened in Excel to see what it contains. What is the risk?
◉ A formula in the workbook can run when the file opens, on the reader's machine.
→ Right. That's why a workbook from outside should be scanned for formulas before it is opened.
○ None, because Excel shows only the values, never the formulas.
→ Excel shows the values, but it also calculates the formulas as the file opens.
○ The file's display format can hide data, but that has no effect on the reader's machine.
→ The format is a display setting. The risk comes from formulas, not from formatting.
```

---
