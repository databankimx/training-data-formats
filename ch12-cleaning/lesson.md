# 12. Cleaning

Cleaning changes data so that it passes its schema. Validation, in the last chapter, only reports problems. Cleaning goes a step further, and it makes changes, which is where most of the risk is. A cleaner that changes a value it should have flagged has made the data look right while being wrong. This chapter covers the rules a careful cleaner follows: fix only what can be fixed without guessing, report what needs a person, keep a record of every change, and never delete a row silently.

The chapter uses the bad files from earlier. `customers-bad-dates.csv` has dates to repair, `customers-null-mix.json` has nulls and an empty name, and `customers-duplicates.csv` repeats two customers, one of them with a different balance. The trimming and date homework use inline data, because no sample file has stray spaces or mixed date styles together.

**Libraries.** No new libraries. C# uses `System.Text.RegularExpressions`, `System.Globalization`, `System.Text.Json`, `CsvHelper` 33.1.0 for reading CSV, and `System.IO`. Python uses the standard `csv`, `json`, `re`, and `os` modules. JavaScript uses `csv-parse`, already pinned, and the built-in `JSON` object, along with `node:fs` and `node:path`.

The chapter has a reading step, four samples, two homework items, and a summary with three quizzes.

---
