# 0. Introduction

Data arrives in files, and the files come in many shapes. A customer list might be a spreadsheet, a comma-separated export, a JSON response from an API, or a configuration file written in YAML. Each shape has its own rules, and most of the bugs that cost time come from the gap between what a file looks like and what a program assumes it says.

This tutorial works through the formats you will meet most often in business systems: JSON, JSON Lines, CSV and TSV, fixed-width text, XML, YAML, Excel, and Parquet. For each one it covers the jobs you actually do: reading, writing, cleaning, converting between formats, serializing and deserializing, and manipulating the rows. Every concept is shown in C#, Python, and JavaScript.

The examples run on real files. A set of sample files, generated from one dataset of customers and orders, is shipped with the tutorial. Some of them are deliberately wrong, with a byte-order mark, the wrong encoding, a truncated file, or a formula hidden in a cell. Learning to spot and handle those is most of the job.

This chapter has two reading steps, a sample step, and a summary with three quizzes. It has no homework, because there is nothing to submit yet. The next chapter starts with text, encodings, and line endings, since every format depends on them.

**Libraries.** No third-party packages. C# uses `System.IO` and `System.Text`, both part of the .NET base libraries. Python uses `os`, from the standard library. JavaScript uses `node:fs` and `node:path`, built into Node.

---
