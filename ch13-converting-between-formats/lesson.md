# 13. Converting Between Formats

Most data work ends with a conversion: a CSV export becomes JSON for an API, a workbook becomes Parquet for analysis, or a fixed-width feed becomes XML for a legacy system. A conversion looks like a copy, but each format can say things the others cannot, so a conversion always keeps a fact, changes its form, or loses it. A careful converter knows which of the three is happening, and checks the result.

This chapter takes the customer data through every format in the tutorial, in a loop. Each link reads the output of the link before it and writes the next format: CSV, TSV, JSON, JSON Lines, XML, YAML, fixed-width, Excel, and Parquet, and then back to CSV. The last link compares the result with the original file, on values and on text. The reading step sets out what each format keeps, changes, or loses, so the pairs of formats can be compared without running seventy-two conversions.

The losses that catch people most often are covered in the samples and the homework: a list that is joined into text, a nested address that is flattened, a postal code that becomes a number, and a decimal balance that becomes a binary float.

**Libraries.** No new libraries. C# uses the libraries each format's chapter already declares: CsvHelper 33.1.0, `System.Text.Json`, `System.Xml.Linq`, YamlDotNet 18.1.0, ClosedXML 0.105.1, and Parquet.Net 5.6.1. Python uses the standard `csv` and `json` modules, `lxml`, `PyYAML`, `openpyxl`, `pyarrow`, and `os`. JavaScript uses `csv-parse`, `csv-stringify`, `fast-xml-parser`, `js-yaml`, `exceljs`, `hyparquet`, and `hyparquet-writer`, all already pinned in `samples\package.json`, along with `node:fs` and `node:path`.

The chapter has a reading step, nine links in a loop, two homework items, and a summary with three quizzes.

---
