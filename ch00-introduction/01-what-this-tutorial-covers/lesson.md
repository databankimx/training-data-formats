# What This Tutorial Covers

Every format in this tutorial answers the same five questions, and the tutorial returns to them in each chapter.

1. **Reading.** How does a program turn the bytes of the file into values it can use?
2. **Writing.** How does it turn values back into bytes that another program will accept?
3. **Cleaning.** What is wrong with the file, and what can be fixed before the rows are used?
4. **Converting.** How do the same values move from one format to another without changing their meaning?
5. **Serializing and manipulating.** How do records become objects in the program, and how are the rows filtered, renamed, grouped, and joined?

The formats are JSON, JSON Lines, CSV and TSV, fixed-width text, XML, YAML, Excel, and Parquet. Chapter 1 covers text, encodings, and line endings, which every other format relies on.

## The sample dataset

The good files all describe the same data: twelve customers and twenty-four orders. A customer has an identifier, a name, an email address, a signup date, a balance, an active flag, a country code, a nested address, and a list of tags. An order has an identifier, the customer it belongs to, a date, an amount, and a status.

Because every good file holds the same data, a conversion can be checked. If you read the JSON file, write it as XML, and read the XML back, the customers should match. A lesson that loses a value along the way will show exactly which value, and in which format.

## The bad files

Some sample files are wrong on purpose. Each one is named for its failure:

- `customers-utf8-bom.csv` starts with a byte-order mark.
- `customers-windows-1252.csv` is encoded in Windows-1252, not UTF-8.
- `customers-mixed-line-endings.csv` mixes CRLF and LF line endings.
- `customers-truncated.json` is cut off partway through.
- `config-norway.yaml` reads the country code `NO` as a boolean.

The rest are listed where they are used. A bad file is never fixed in place. Your code deals with it, and the lesson shows what the fix does.

> **Aside: why the bad files matter.** Most real data problems are quiet. The program runs, the output looks plausible, and one value is wrong. The bad files are there so you can see that failure on purpose, before it happens to you on a real file.

---
