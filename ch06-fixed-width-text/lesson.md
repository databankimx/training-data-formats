# 6. Fixed-Width Text

Fixed-width text has no delimiter at all. Each record is one line, and each field lives at a set position: the customer identifier is always in columns 1 to 6, the name in 8 to 27, and so on. The layout is the only description of the file, so the file is useless without it. Many government feeds, bank statements, and older mainframe exports still use this shape, because a fixed layout is compact and easy to read by position.

The format's weakness is the same as its strength. Nothing marks where a field ends except the position, so a short line, a value wider than its column, or a multibyte character can move everything after it without any error. The chapter covers reading and writing by position, the difference between counting bytes and counting characters, a short line, and the rules that keep a layout safe.

The sample files are `customers.fixed`, which holds the twelve customers, and `customers.fixed.layout.txt`, which describes the columns. `customers-fixed-short-row.fixed` has one line cut short. Here is the first two lines of `customers.fixed`, with a ruler above them that counts positions from 1:

```text
         1         2         3         4         5
12345678901234567890123456789012345678901234567890123456
  1001 Alice Carter         2021-03-14  1250.75 true  US
  1002 Okafor, Chidi        2020-11-02     0.00 false GB
```

Each line is 56 characters, and every value sits under its column. The identifier ends at column 6, the name starts at column 8, and the balance ends at column 47.

**Libraries.** No third-party packages, and no fixed-width parser. Fixed-width is read by position in each language, with the standard string functions. C# uses `System.IO`, Python uses `os`, and JavaScript uses `node:fs` and `node:path`, all built in. The layout is written out in each sample, so the positions stay visible in the code.

The chapter has a reading step, four samples, two homework items, and a summary with three quizzes.

---
