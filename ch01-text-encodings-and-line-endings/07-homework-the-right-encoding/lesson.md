# Homework: Read the File with the Right Encoding

The file `customers-windows-1252.csv` in the sample data folder is Windows-1252, not UTF-8. The sample in step 3 read it as UTF-8 and found four replacement characters. This homework reads it with the encoding it was written in.

Write a program that reads the file as Windows-1252 and prints one line:

`Lines containing e-acute: ` followed by the number of lines that contain the letter é, the accented e with code point U+00E9.

Read the file from the folder named by `TRAINING_DATA`. Don't write its path into the code.

Give the letter as the escape `\u00e9`, so the source file itself is plain ASCII. Count lines, not occurrences: a line with the letter twice still counts once.

The expected output is:

~~~text
Lines containing e-acute: 1
~~~

Two things make this homework harder than it looks. First, the decoding has to be Windows-1252, and a program that decodes as UTF-8 won't find the letter at all, because the byte for é is not a UTF-8 character. It prints 0 and no error. Second, the C# runtime doesn't include Windows-1252 unless the program registers the code-page provider before it asks for the encoding. The C# starter shows where that registration goes.

The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
