# Homework: Detect Three Files

Write a detector, and use it on three sample files from the data folder. Read each file from the folder named by `TRAINING_DATA`, and don't write its path into the code.

The three files are, in this order:

1. `customers.parquet`
2. `customers.xlsx`
3. `customers-as-json.csv`

Check the signatures in the order from the first step: Parquet first, then zip, then OLE2, then JSON, then XML, then binary or text. The first match gives the kind. For each file, print one line:

`<file name>: <kind>`

The expected output is:

~~~text
customers.parquet: parquet
customers.xlsx: zip
customers-as-json.csv: json
~~~

Check compares your output with that, and ignores line endings and trailing spaces.

Two things to get right. The JSON check has to skip any whitespace before the bracket, and it must not report a file as text just because its name ends in `.csv`. The detector looks at the bytes only. The name plays no part in the answer, which is the point of the chapter.

The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
