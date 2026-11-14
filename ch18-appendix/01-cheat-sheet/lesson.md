# Cheat Sheet

Use this page when you need the library for a format in one language. The names below are the libraries the tutorial pins, so the code in a lesson and the code you write later use the same tools. A version number in the table is the version the sample was tested with.

## Libraries by format

| Format | C# | Python | JavaScript |
| --- | --- | --- | --- |
| JSON | System.Text.Json | json (standard library) | JSON.parse and JSON.stringify |
| JSON Lines | System.Text.Json, one line at a time | json, one line at a time | JSON.parse, one line at a time |
| CSV and TSV | CsvHelper 33.1.0 | csv (standard library) | csv-parse 7.0.2, csv-stringify 6.8.3 |
| Fixed-width text | No library: slice by column position | No library: slice by column position | No library: slice by column position |
| XML | System.Xml.Linq | lxml 6.1.0 | fast-xml-parser 5.12.1 |
| YAML | YamlDotNet 18.1.0 | PyYAML 6.0.3 | js-yaml 5.4.1 |
| Excel .xlsx | ClosedXML 0.105.1 | openpyxl 3.1.5 | exceljs 4.4.0 |
| Excel .xls (legacy) | Not covered | xlrd 2.0.1 | Not covered |
| Parquet | Parquet.Net 5.6.1 | pyarrow 26.0.1 | hyparquet 1.26.2 to read, hyparquet-writer 0.15.6 to write |

The legacy .xls format is read only in Python, because that is the one language the tutorial has a reader for. The xlwt library is used by the sample generator to make the .xls sample file, and it is not a dependency of any lesson.

## Reading a text file

Name the encoding every time you open a text file. The tutorial uses UTF-8 throughout, and a file in another encoding should be opened with that encoding, not with the default. Check for a byte-order mark at the start of the file, and remove it before you parse the text. Chapter 1 shows both checks.

## Before you trust a file

Work through this list before the rows are used. Each item is a failure a chapter showed.

- Encoding: is the file UTF-8, and is there a byte-order mark? (Chapter 1)
- Line endings: are they all CRLF, all LF, or mixed? (Chapter 1)
- Format: does the content match the extension? (Chapter 2)
- Delimiter and quoting: does a quoted field contain a newline or a delimiter? (Chapter 5)
- Row length: does every row have the same number of fields? (Chapter 5)
- Numbers stored as text: does a column that should be numeric hold text? (Chapter 9)
- Formula cells: does a text value begin with a formula character? (Chapter 16)
- Dates: are they in one format, and is each one a real date? (Chapters 11 and 12)
- Nulls and missing keys: does the file use null, an empty string, or no key at all? (Chapters 3 and 11)
- External references: does an XML file contain a DOCTYPE or an external entity? (Chapter 7)
- Country codes: is any value, such as NO, read as something other than text? (Chapter 8)

> **Aside: the list is short on purpose.**
> A longer list would be easier to skip. Each item here has a sample file that fails it, so you can check each one against a real case.

> **Common mistake.** Checking only that the program runs. A file that parses without error can still have a wrong encoding, a shifted column, or a number that became text. The list above is about the values, not the parse.

---
