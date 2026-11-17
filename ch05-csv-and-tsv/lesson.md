# 5. CSV and TSV

CSV is the oldest format in this tutorial and the one most often misread. It's a table written as text: one record per line, fields separated by commas, and a header line that names the columns. Spreadsheets export it, databases dump it, and most business systems accept it. Its simplicity is the trap. A comma inside a name, a quote inside a note, or a line break inside an address all break a naive reader, and CSV has no type information to catch the mistake.

TSV is the same format with tabs for separators. It's a useful variant, because a tab rarely appears in data, so fields usually need no quoting.

This chapter covers what the format's rules are, reading and writing with quoting, embedded newlines, ragged rows, formula cells, and TSV. The sample files are `customers.csv`, which holds the twelve customers, and `customers.tsv`, which holds the same data with tabs. Three more files show the failures: `customers-embedded-newline.csv` has a line break inside a quoted field, `customers-ragged.csv` has rows with the wrong number of fields, and `customers-formula.csv` has a cell that a spreadsheet would run.

## What the format looks like

These are the header and the second customer in `customers.csv`. The name `Okafor, Chidi` contains a comma, so it's in quotes. The other eleven customers follow the same shape.

```csv
customer_id,name,email,signup_date,balance,active,country_code,address_street,address_city,address_postal_code,tags
1002,"Okafor, Chidi",chidi.okafor@example.invalid,2020-11-02,0.00,false,GB,14 Harbour Road,Bristol,BS1 4DJ,
```

The same two rows in `customers.tsv` look like this. The separators are tabs, and the name needs no quotes, because a comma is ordinary text in a tab-separated file.

```tsv
customer_id	name	email	signup_date	balance	active	country_code	address_street	address_city	address_postal_code	tags
1002	Okafor, Chidi	chidi.okafor@example.invalid	2020-11-02	0.00	false	GB	14 Harbour Road	Bristol	BS1 4DJ	
```

Notice that every value is text. The balance `0.00` and the postal code `BS1 4DJ` look the same to the file, and only the reader decides what each one means. The empty last field, after the final comma or tab, is an empty tags value, which is different from a missing field.

**Libraries.** Python uses the standard `csv` module and `os`. C# uses CsvHelper 33.1.0 (Apache-2.0, declared in each sample with a `#:package` line), along with `System.IO` and `System.Linq`. JavaScript uses `csv-parse` 7.0.2 and `csv-stringify` 6.8.3 (both MIT), declared in `samples\package.json`, along with `node:fs`, `node:path`, and `Buffer`. Install the JavaScript packages with `npm install` in `samples` before running the JavaScript samples.

The chapter has a reading step, six samples, two homework items, and a summary with three quizzes.

---
