# What CSV Is

A CSV file is a grid of text. Each line is a record, and within a record the fields are separated by a delimiter, normally a comma. The first line is usually a header that names the columns. Nothing in the file says what a value means: `0.00` is text until a reader decides it's a number, and `2021-03-14` is text until a reader decides it's a date.

The format has a short set of rules, which the 2005 RFC 4180 describes. A field that contains the delimiter, a double quote, or a line break must be wrapped in double quotes. A double quote inside a quoted field is written as two double quotes. A line break inside a quoted field doesn't end the record. Every record should have the same number of fields as the header. A file usually ends with a line break, and some writers add a byte-order mark at the start.

The rules are easy to state and easy to break. Many programs split each line on commas, and that works until the first name `Okafor, Chidi` appears. The split then gives two fields where the file has one, and every value after it shifts one column to the right. The record looks plausible, and the error is in the data's shape, not its content.

Quoting is what keeps the shape. A correct reader handles a quote as a switch: inside quotes, a comma is ordinary text, and outside quotes it separates fields. A correct writer does the reverse, quoting only the fields that need it. The samples in this chapter show both.

Two things that CSV doesn't do matter as much. It has no types, so every reader has to decide what `62704` is. It has no standard for a decimal comma, so a file written in a country that uses one may use semicolons and commas in a way that a comma-delimited reader misreads. The format is simple to produce and easy to misread.

> **Aside: TSV is CSV with tabs.**
> A tab-separated file follows the same rules with a tab as the delimiter. Tabs are rare in real data, so fields seldom need quoting. The TSV sample at the end of the chapter shows the difference.

> **Common mistake.** Splitting each line on commas. It looks right on the first line, breaks on a quoted comma, and then quietly moves every later value into the wrong column. Use a parser that understands quotes.

---
