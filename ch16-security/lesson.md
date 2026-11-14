# 16. Security With Untrusted Input

Every file in this tutorial is one the author made, so each sample could trust its input. A file from a customer, a partner, or a web form cannot be trusted that way. It can be large, deeply nested, full of entities that point at files, carry formulas that run when a spreadsheet opens it, or hold text that ends up in a log and makes the log misleading. This chapter covers the defences: refusing input that is too big, neutralising values that a spreadsheet would run, limiting how many records are read, and logging problems without copying the untrusted value into the log.

Two of the attacks in the roadmap are described here and not generated. One is an XML file that expands exponentially when a parser resolves its entities. The other is a compressed archive that expands to a very large size. Generating either would leave a harmful file in the repository, so the lesson describes what each one does and shows the defence in code that refuses it. The external-entity defence was covered in the XML chapter, and the formula defence in the CSV and Excel chapters, so this chapter draws those together into a set of rules for any input.

**Libraries.** No new libraries. C# uses `System.IO`, `System.Text`, and `System.Linq`, and CsvHelper 33.1.0 where a sample reads CSV. Python uses the standard `csv`, `json`, `os`, and `re` modules. JavaScript uses `node:fs`, `node:path`, and `csv-parse`, already pinned in `samples\package.json`.

The chapter has a reading step, four samples, two homework items, and a summary with three quizzes.

---
