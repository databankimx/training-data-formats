# 2. Detecting a Format

A file's name says what the file is supposed to be. The content says what it is. Usually the two agree, and a program can trust the extension. When they don't agree, a program that trusts the name will read the bytes as the wrong format, and the error may be far from the cause. A file exported as `customers.csv` that is really JSON is one example, and a spreadsheet saved under a `.txt` name is another.

This chapter teaches detection by content. Every format starts with a few bytes that identify it, called a signature or magic bytes, and a program can read those bytes before it commits to a reader. The chapter covers the signatures for Parquet, Excel (both the modern zip-based format and the legacy binary one), JSON, and XML, the order in which a detector should check them, and what detection can and can't tell you. Detection tells you the kind of file. It doesn't tell you the file is valid, so a truncated JSON file is still JSON.

The chapter has a reading step, two samples, two homework items, and a summary with three quizzes. The samples read sample files and print what they find. The first homework item builds a detector, and the second adds the byte-order mark to it.

**Libraries.** No third-party packages. C# uses `System.IO`, `System.Text`, and `System.Linq`, all part of the .NET base libraries. Python uses `os`. JavaScript uses `node:fs`, `node:path`, and `Buffer`, all built into Node.

---
