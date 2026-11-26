# DataBank IMX - Working With Data Formats

## License and Support

This repository is provided under the [MIT License](LICENSE). You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell the materials in this repository, subject to the terms of that license.

This repository is provided for training and reference purposes only. DataBank IMX does not provide warranties, guarantees, maintenance, troubleshooting, implementation assistance, or technical support for this code or its use. Use it in any way permitted by the MIT License, but you are responsible for evaluating, adapting, testing, and supporting any use of it in your own environment.

---

## What is this repository for?

* A tutorial on reading, writing, cleaning, converting, serializing, and manipulating data in the formats most often found in business systems: JSON, JSON Lines, CSV and TSV, fixed-width text, XML, YAML, Excel, and Parquet
* Each format is worked through in C#, Python, and JavaScript, using real sample files
* Some sample files are wrong on purpose, so you can see the failure before it happens to you
* A desktop lesson runner (Windows) that shows each lesson, runs its code, and checks the exercises

---

## Who is this for?

* DataBank IMX developers who read, write, or convert data files as part of their work
* Developers who want to understand how data goes wrong in each format and how to handle it

**Prerequisites**

* This is a standalone tutorial. It needs no other tutorial in this collection first.
* Some familiarity with a scripting language is helpful, because every exercise is a short program

---

## About

* **Author:** [Scott McLean](mailto:smclean@databankimx.com)
* **Purpose:** Internal developer training on data formats at DataBank IMX

---

## DataBank Responsibilities for Custom Code

All DataBank employees - including those working with AI-assisted tools - are bound by the Development Rules of Engagement, published as the [development-rules-of-engagement.pdf](https://databankimx.sharepoint.com/:b:/r/sites/Hub-PS/DevTools/Policies/development-rules-of-engagement.pdf?d=w1c01477e09e048acbe4c96eba851a183&csf=1&web=1&e=uL7JEw). That document defines the rules for quoting, approving, developing, reviewing, scanning, storing, and delivering custom code for client work.

Key obligations that apply to everyone on every custom code engagement:

* **You own the code you deliver.** This applies equally to hand-written code, AI-assisted code, and AI-generated code. "The AI wrote it" is not an acceptable explanation for a production issue, a failed review, a security finding, or a support problem.
* **Code must be reviewed before delivery.** Review is interactive and must confirm that the code works, meets DataBank standards, is maintainable, and that the developer understands it well enough to explain, debug, and maintain it. Polished or well-formatted output - including AI-generated output - is not evidence of correctness.
* **Code must be in source control before delivery.** All custom code must be committed to the appropriate DataBank GitHub Enterprise repository before it is delivered to a client, regardless of whether the client receives source code, compiled binaries, or deployed functionality.
* **CI scanning must pass before delivery.** Required checks are the standards policy scan, SonarQube, and Snyk. A passing local build is not a substitute.
* **All third-party dependencies must be license-vetted.** The license must permit closed-source commercial use. Copyleft or unclear licensing must be escalated before use. Dependencies must not be added simply because an AI tool suggested them.
* **Only approved AI tools may be used.** Use only IT-approved tools through company accounts. All data entered into AI systems is subject to the [DataBank AI Acceptable Use Policy](https://workforcenow.adp.com/mascsr/wfncontenttools/file-management/file/JTJGc3RhdGljJTJGY2xpZW50cyUyRmNvbnRlbnQlMkZBSStBY2NlcHRhYmxlK1VzZStQb2xpY3kucGRmJTNGMTc3MTM0NzA4NjE4MQ==) and must be treated as confidential by default.
* **Custom code is billable work.** Code must be tied to an approved quote or engagement before commitment or delivery. Development quotes require approval from the Development Director or delegated development leadership before being sent externally.
* **Exceptions require explicit approval.** Time pressure alone is not a reason to bypass quote approval, source control, review, or CI scanning.

See the Development Rules of Engagement linked above for the full policy, including billing and quoting rules, source-code delivery rules, the delivery readiness checklist, and the exception process.

> Policy document links point to DataBank internal locations. They may not open for readers outside DataBank IMX.

---

## Setup and requirements

The tutorial is at [databankimx/training-data-formats](https://github.com/databankimx/training-data-formats). Run the setup script once from the tutorial's folder, then start the runner. The script installs what's missing, creates the Python virtual environment, and installs the packages for the samples and the runner:

```pwsh
powershell -NoProfile -ExecutionPolicy Bypass -File .\setup.ps1
cd lesson-runner
npm start
```

[QUICKSTART.md](QUICKSTART.md) has the details, including the manual steps if you'd rather not run the script, how the runner works, where your progress is saved, and how to fix common problems.

* Windows 10 or 11
* Git, for cloning the repository
* Node.js 24 or later, for the runner and the JavaScript samples
* Python 3.12 or later, for the Python samples
* The .NET 10 SDK, for the C# samples
* The Visual Studio Build Tools with the C++ workload, the fallback if Electron's download fails

The setup script installs anything that's missing. The Build Tools need an Administrator PowerShell.

---

## Third Party Licenses

Each library used in this repository is listed below. Check each library's license file before you use it outside this repository.

| Component | License | Used for |
|---|---|---|
| Electron | MIT | The runner's desktop window |
| markdown-it | MIT | Rendering lesson Markdown |
| highlight.js | BSD-3-Clause | Coloring code in the lessons and the editor |
| csv-parse, csv-stringify | MIT | JavaScript CSV samples |
| exceljs | MIT | JavaScript Excel samples |
| fast-xml-parser | MIT | JavaScript XML samples |
| hyparquet, hyparquet-writer | MIT | JavaScript Parquet samples |
| js-yaml | MIT | JavaScript YAML samples |
| uuid | MIT | Transitive dependency, pinned by an override |
| PyYAML | MIT | Python YAML samples |
| openpyxl, et_xmlfile | MIT | Python Excel samples |
| pyarrow | Apache 2.0 | Python Parquet samples |
| xlrd, xlwt | BSD | Python legacy .xls samples |
| lxml | BSD-3-Clause | Python XML samples. The wheel also bundles GPL-2.0-only components, which need review before commercial use |
| colorama, iniconfig, packaging, pluggy, Pygments | BSD, MIT, or Apache 2.0 | Test support, pulled in by pytest |
| pytest | MIT | Tests |
| ClosedXML | MIT | C# Excel samples |
| CsvHelper | Apache 2.0 | C# CSV samples |
| Parquet.Net | MIT | C# Parquet samples |
| YamlDotNet | MIT | C# YAML samples |

---

## Running the tutorial

The runner is a desktop window that shows each lesson, lets you choose the language tab, and runs the code in C#, Python, and JavaScript. Press **Run** to run your code, or **Check** to compare its output with the expected result. [QUICKSTART.md](QUICKSTART.md) describes the runner in full.

---

## Repository structure

```
training-data-formats/
|- ch00-introduction/ to ch17-testing-with-fixtures/   - Chapters, each with lesson.md and step folders
|- ch18-appendix/                                     - Cheat sheet, format guide, and glossary
|- lesson-runner/                                     - Electron desktop runner
|- samples/                                           - Sample data, sample packages, and run folders
|- resources/                                         - Design notes (internal, not published)
|- requirements.txt                                   - Python packages for the learner
|- setup.ps1
|- QUICKSTART.md
```

Each step folder has a `lesson.json` and a `lesson.md`. Each chapter has a short introduction, a few sample steps, a second reading step, two homework items, and a summary with three quizzes. The appendix has no quizzes and no homework.

### Chapters

| Chapter | Topic |
|---|---|
| 00 Introduction | What the tutorial covers, the sample dataset, and how the sample files are found. No exercise |
| 01 Text, Encodings, and Line Endings | UTF-8, byte-order marks, Windows-1252, and mixed line endings |
| 02 Detecting a Format | Deciding a format from its content, because a file name can lie |
| 03 JSON | Reading and writing, nulls, nested objects, large integers, and a defective file |
| 04 JSON Lines | One record per line, reading a stream, and a file with one malformed line |
| 05 CSV and TSV | Delimiters, quoting, embedded newlines, ragged rows, and formula cells |
| 06 Fixed-Width Text | Columns by position, and a row that is too short |
| 07 XML | Elements, attributes, namespaces, and an external entity |
| 08 YAML | Mappings, lists, typed values, the Norway problem, and tabs |
| 09 Excel | Workbooks, numbers stored as text, formula cells, and the legacy .xls format |
| 10 Parquet | Columns, types, nested columns, and nullable values |
| 11 Schemas and Validation | Checking each file against a schema, including dates that fail |
| 12 Cleaning | Trimming whitespace, filling nulls, fixing dates, and removing duplicates |
| 13 Converting Between Formats | One dataset carried through a chain of formats, and compared at each step |
| 14 Serialization | Reading records into objects and writing them back, and unknown fields |
| 15 Manipulation | Filtering, renaming and computing, grouping, and joining customers with orders |
| 16 Security with Untrusted Input | External entities, formula cells, oversized input, and safe logging |
| 17 Testing with Fixtures | Round-trip tests, golden-file tests, and refusal tests |
| 18 Appendix | A cheat sheet, a format guide, and a glossary |

### Sample data

Every good sample file describes the same data: twelve customers and twenty-four orders. A conversion can be checked by comparing the result with the original. The bad sample files are named for their failure, and a bad file is never fixed in place. Your code deals with it, and the lesson shows what the fix does.

The samples read their files through the `TRAINING_DATA` environment variable, which the runner sets to `samples\data`. A sample that types its data into the code says so in a comment that begins "Inline data, not from a sample file."

---

## Known conflicts and compatibility notes

* The runner and the setup script run on Windows only.
* The first run of a C# sample downloads its NuGet packages, so it needs internet access.
* The bad sample files are malformed on purpose. Some steps show a failure until your code handles it.
* The Visual Studio Build Tools are the fallback when Electron's download fails, and installing them needs an Administrator PowerShell.

---

## Authorship note

This tutorial was written by me for internal use at DataBank. As with the other training repositories, I used generative AI in places for code review, cleanup, and turning rough notes into readable documentation.

~ Scott McLean, 2026

---

## Release version

| Date | Changes |
|---|---|
| 11/17/2026 | Initial release: Chapters 0 to 18 with the lesson runner, the sample data, and the setup script |

---

## Contact

* [Scott McLean](mailto:smclean@databankimx.com)
* [Dev Team](mailto:development@databankimx.com)
