# Homework: The Byte-Order Mark and Text

A text file can start with a byte-order mark: the three bytes `EF BB BF`. The mark doesn't change what the file is. A file with the mark is still text, but a reader that wants to know whether to skip the mark needs to know it's there.

Write a program that checks three sample files in this order, and prints one line for each:

1. `customers-utf8-bom.csv`
2. `customers-windows-1252.csv`
3. `config-norway.yaml`

For each file, print `<file name>: text`. If the file starts with the three bytes `EF BB BF`, add `, with byte-order mark` to the end of the line. Read each file from the folder named by `TRAINING_DATA`.

The expected output is:

~~~text
customers-utf8-bom.csv: text, with byte-order mark
customers-windows-1252.csv: text
config-norway.yaml: text
~~~

Check compares your output with that, and ignores line endings and trailing spaces.

Two things to get right. The mark is checked on the bytes, before any decoding, so a reader that strips it doesn't hide it from the check. And the Windows-1252 file must come out as text without the mark. It has no NUL byte, so it's text, even though its bytes aren't valid UTF-8. That's a detection result, not a decoding one.

The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
