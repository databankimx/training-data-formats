# 11. Schemas and Validation

A schema is a written statement of what a file should contain: the columns, the type of each value, which values may be missing, and which values are allowed. A file that matches its schema can be trusted to mean what the schema says. A file that doesn't match has a problem, and the problem should be reported with its location, not discovered later as a wrong total or a crash. This chapter covers writing a schema as a set of rules, checking a file against it, and reporting every failure with its line or record.

The chapter uses the customer data from the earlier chapters. The clean file `customers.csv` should pass every rule. `customers-bad-dates.csv` fails on dates, `customers-null-mix.json` fails on nulls and missing keys, and `customers-duplicates.csv` repeats identifiers. The homework checks a line-based file, `orders-lines.jsonl`, which has one malformed line.

The schema is written out inside each sample, as literal data, so the rules are visible where they're used. Each sample comments the schema, as the inline-data convention requires.

**Libraries.** No new libraries. C# uses CsvHelper 33.1.0 (Apache-2.0, declared with `#:package`) for reading CSV, `System.Text.Json` for JSON, and `System.IO`. Python uses the standard `csv`, `json`, `datetime`, and `os` modules. JavaScript uses `csv-parse`, already pinned in `samples\package.json`, and the built-in `JSON` object, along with `node:fs` and `node:path`.

The chapter has a reading step, three samples, two homework items, and a summary with three quizzes.

---
