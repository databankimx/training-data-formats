# 14. Serialization and Deserialization

Serialization turns a value in a program into text or bytes that another program can read, and deserialization does the reverse. Most programs don't work on a file's raw structure. They work on records with names and types: a customer with a balance, an address, and a list of tags. Serialization is the mapping between that record and its file form, and most of the bugs in a data pipeline sit in that mapping, not in the file itself.

This chapter maps the customer records to classes and back. It covers reading a JSON array into typed records, writing the records out and reading them back, and deciding what to do with a field the program doesn't know. The unknown-field sample is the important one: a file from another system often carries fields the program was never written for, and the decision to ignore, report, or refuse them is a design choice that should be made on purpose.

The sample data is `customers.json`, which the earlier chapters used, and the samples define their classes inline, so the mapping is visible where it's used.

The chapter uses JSON throughout, but the same decisions apply to every format in this tutorial. A serializer could be written for CSV, XML, YAML, Excel, Parquet, or any other format. JSON was chosen because each language already ships a serializer for it, so the chapter can spend its time on the decisions rather than the mechanics.

**Libraries.** No new libraries. C# uses `System.Text.Json`, which ships with .NET, and `System.IO`. Python uses the standard `json`, `dataclasses`, `decimal`, and `os` modules. JavaScript uses the built-in `JSON` object, along with `node:fs` and `node:path`.

The chapter has a reading step, three samples, two homework items, and a summary with three quizzes.

---
