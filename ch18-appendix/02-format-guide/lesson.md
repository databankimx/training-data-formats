# Format Guide

No format is right for every job. This guide sets out what each format is for, where it tends to go wrong, and which chapter shows the failure. Read it when you are choosing a format for a new file, or deciding whether a file you have been given is in the right one.

## JSON

Use JSON for nested data that a program reads and writes, such as an API response or a configuration with objects inside objects. It has types: strings, numbers, booleans, nulls, arrays, and objects.

Be careful with numbers. JSON does not say how big an integer may be, and a parser may round a large one. JavaScript stores numbers as 64-bit floats, so an integer above 2 to the power of 53 can change without an error. Chapter 3 shows the case. JSON is a poor choice for a spreadsheet, because it has no rows.

## JSON Lines

Use JSON Lines for a large file of records that is written and read a line at a time, or that grows by appending. Each line is one complete JSON value, so a program can read the file without loading all of it, and a malformed line damages only that line. Chapter 4 covers this.

Be careful with a file that is cut off or has one bad line. The last line may be incomplete, and a reader has to decide whether to refuse the file or skip the line. Chapter 4 shows a malformed line, and the choice between those two responses is yours to make for your own data.

## CSV and TSV

Use CSV or TSV for a table that people will open in a spreadsheet, or that another program expects in this form. Both are simple, and nearly every tool reads them. TSV is CSV with tabs for separators, and it is less likely to need quoting because tabs rarely appear in data.

Be careful with everything the format does not say. CSV has no types, so a date and a number are both text. A quoted field may hold a comma or a newline. A row may have too few or too many fields. A cell that begins with a formula character can run as a formula when the file is opened. Chapters 5, 9, and 16 cover these.

## Fixed-width text

Use fixed-width text when a legacy system or an older bank or government file defines each field by its column position. There are no separators, so a field is found by where it sits in the line.

Be careful with bytes and characters. A column measured in bytes is not the same as a column measured in characters once the text has accented letters. A short row, one that ends before the last field, is easy to miss. Chapter 6 shows both.

## XML

Use XML for documents with a defined structure, namespaces, or attributes, and for systems that already exchange XML. It can say more than CSV or JSON, at the cost of length.

Be careful with external entities. XML can refer to a file or a network address, and a parser that resolves the reference reads that file. The tutorial's samples refuse these references, and Chapter 7 shows the three outcomes. Do not treat the file as trusted because it came from a partner.

## YAML

Use YAML for configuration that people edit by hand, because it is easy to read and allows comments. Indentation sets the structure, which is why it suits settings files.

Be careful with indentation, which must use spaces, because a tab is refused by the parsers in this tutorial. Be careful with unquoted values: the country code NO is read as a boolean false in YAML 1.1, which is what PyYAML and older YAML libraries do. Chapter 8 covers both, under the name the Norway problem.

## Excel

Use Excel for a table that people will read, edit, sort, or calculate with. A workbook can hold several sheets, formatting, and formulas.

Be careful with numbers stored as text. A value that looks like a number may have been typed or pasted as text, and a sum over that column will ignore it. Formula cells hold a formula and a result, and a reader may give you either one, depending on the library. The legacy .xls format is older and has fewer rows. Chapter 9 covers these.

## Parquet

Use Parquet for large tables read for analysis. It stores each column together, so a query that needs three columns of thirty reads only those three. It is compressed, and it keeps types, so a date stays a date.

Be careful because Parquet is not readable as text. You need a library, or a viewer such as the one Chapter 10 links to, to see its contents. A column that allows missing values must say so in the reader, or the file fails to read. Chapter 10 shows this with the C# library.

## Choosing

If the data is nested and a program will read it, choose JSON. If it is a large list of records that grows over time, choose JSON Lines. If people will open it in a spreadsheet, choose CSV or Excel. If it is a configuration, choose YAML. If it is a document or it must match an XML schema, choose XML. If it is a large table for analysis, choose Parquet. If a legacy system defines it by column position, use fixed-width text, and read it as the system specifies.

> **Aside: the format decides what can go wrong.**
> A CSV file can have a formula, a YAML file can have a boolean where you expected a country code, and an XML file can reach outside itself. Knowing the format tells you which of these to check.

> **Common mistake.** Choosing a format because it is familiar. A team that always writes CSV may find that a nested address has to be flattened into dotted columns, and that the flattening loses which fields belonged together. Choose the format from the shape of the data.

---
