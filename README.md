# Working With Data Formats

## License and Support

This repository is provided under the [MIT License](LICENSE). You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell the materials in this repository, subject to the terms of that license.

This repository is provided for training and reference purposes only. DataBank IMX does not provide warranties, guarantees, maintenance, troubleshooting, implementation assistance, or technical support for this code or its use. Use it in any way permitted by the MIT License, but you are responsible for evaluating, adapting, testing, and supporting any use of it in your own environment.

## DataBank Responsibilities for Custom Code

All DataBank employees - including those working with AI-assisted tools - are bound by the [Development Rules of Engagement](development-rules-of-engagement.md). That document defines the rules for quoting, approving, developing, reviewing, scanning, storing, and delivering custom code for client work.

Key obligations that apply to everyone on every custom code engagement:

- **You own the code you deliver.** This applies equally to hand-written code, AI-assisted code, and AI-generated code. "The AI wrote it" is not an acceptable explanation for a production issue, a failed review, a security finding, or a support problem.
- **Code must be reviewed before delivery.** Review is interactive and must confirm that the code works, meets DataBank standards, is maintainable, and that the developer understands it well enough to explain, debug, and maintain it. Polished or well-formatted output - including AI-generated output - is not evidence of correctness.
- **Code must be in source control before delivery.** All custom code must be committed to the appropriate DataBank GitHub Enterprise repository before it is delivered to a client, regardless of whether the client receives source code, compiled binaries, or deployed functionality.
- **CI scanning must pass before delivery.** Required checks are the standards policy scan, SonarQube, and Snyk. A passing local build is not a substitute.
- **All third-party dependencies must be license-vetted.** The license must permit closed-source commercial use. Copyleft or unclear licensing must be escalated before use. Dependencies must not be added simply because an AI tool suggested them.
- **Only approved AI tools may be used.** Use only IT-approved tools through company accounts. All data entered into AI systems is subject to the [DataBank AI Acceptable Use Policy](https://workforcenow.adp.com/mascsr/wfncontenttools/file-management/file/JTJGc3RhdGljJTJGY2xpZW50cyUyRmNvbnRlbnQlMkZBSStBY2NlcHRhYmxlK1VzZStQb2xpY3kucGRmJTNGMTc3MTM0NzA4NjE4MQ==) and must be treated as confidential by default.
- **Custom code is billable work.** Code must be tied to an approved quote or engagement before commitment or delivery. Development quotes require approval from the Development Director or delegated development leadership before being sent externally.
- **Exceptions require explicit approval.** Time pressure alone is not a reason to bypass quote approval, source control, review, or CI scanning.

See the [Development Rules of Engagement](development-rules-of-engagement.md) for the full policy, including billing and quoting rules, source-code delivery rules, the delivery readiness checklist, and the exception process.

---

Data is only as trustworthy as the program that reads it. This tutorial teaches reading, writing, cleaning, converting, serializing, and manipulating data in the formats most often found in business systems: JSON, JSON Lines, CSV and TSV, fixed-width text, XML, YAML, Excel, and Parquet. Each format is worked through in C#, Python, and JavaScript, using real sample files, including some that are wrong on purpose so you can see the failure before it happens to you.

## Quick start

The tutorial is at [databankimx/training-data-formats](https://github.com/databankimx/training-data-formats). Run the setup script once from the tutorial's folder, then start the runner. The script installs what's missing, creates the Python virtual environment, and installs the packages for the samples and the runner:

```pwsh
powershell -NoProfile -ExecutionPolicy Bypass -File .\setup.ps1
cd lesson-runner
npm start
```

[QUICKSTART.md](QUICKSTART.md) has the details, including the manual steps if you'd rather not run the script, how the runner works, where your progress is saved, and how to fix common problems.

## What you need

- Windows 10 or 11
- Git, for cloning the repository
- Node.js 24 or later, for the runner and the JavaScript samples
- Python 3.12 or later, for the Python samples
- The .NET 10 SDK, for the C# samples
- The Visual Studio Build Tools with the C++ workload, the fallback if Electron's download fails

The setup script installs anything that's missing. The Build Tools need an Administrator PowerShell.

The C# samples download their NuGet packages the first time they run, so the first run of a C# sample needs internet access.

## The chapters

Work through them in order. Each chapter has a short introduction, a few sample steps, a second reading step, two homework items, and a summary with three quizzes. The appendix has no quizzes and no homework.

0. **Introduction.** What the tutorial covers, the sample dataset, and how the sample files are found. No exercise.
1. **Text, encodings, and line endings.** UTF-8, byte-order marks, Windows-1252, and mixed line endings.
2. **Detecting a format.** Deciding a format from its content, because a file name can lie.
3. **JSON.** Reading and writing, nulls, nested objects, large integers, and a defective file.
4. **JSON Lines.** One record per line, reading a stream, and a file with one malformed line.
5. **CSV and TSV.** Delimiters, quoting, embedded newlines, ragged rows, and formula cells.
6. **Fixed-width text.** Columns by position, and a row that is too short.
7. **XML.** Elements, attributes, namespaces, and an external entity.
8. **YAML.** Mappings, lists, typed values, the Norway problem, and tabs.
9. **Excel.** Workbooks, numbers stored as text, formula cells, and the legacy .xls format.
10. **Parquet.** Columns, types, nested columns, and nullable values.
11. **Schemas and validation.** Checking each file against a schema, including dates that fail.
12. **Cleaning.** Trimming whitespace, filling nulls, fixing dates, and removing duplicates.
13. **Converting between formats.** One dataset carried through a chain of formats, and compared at each step.
14. **Serialization.** Reading records into objects and writing them back, and unknown fields.
15. **Manipulation.** Filtering, renaming and computing, grouping, and joining customers with orders.
16. **Security with untrusted input.** External entities, formula cells, oversized input, and safe logging.
17. **Testing with fixtures.** Round-trip tests, golden-file tests, and refusal tests.
18. **Appendix.** A cheat sheet, a format guide, and a glossary.

## The sample data

Every good sample file describes the same data: twelve customers and twenty-four orders. A conversion can be checked by comparing the result with the original. The bad sample files are named for their failure, and a bad file is never fixed in place. Your code deals with it, and the lesson shows what the fix does.

The samples read their files through the `TRAINING_DATA` environment variable, which the runner sets to `samples\data`. A sample that types its data into the code says so in a comment that begins "Inline data, not from a sample file."

## Conventions used in this tutorial

The lessons follow a few rules that make documents easier to review:

- Use hyphens, not em dashes.
- Use plain text symbols, not emojis.
- End each lesson with a horizontal rule.

These are good habits in any document, not only in this tutorial.

## Folder layout

- `setup.ps1` prepares the tutorial and installs its packages.
- `QUICKSTART.md` explains setup and the runner.
- `ch00-introduction\` through `ch18-appendix\` hold the chapters. Each chapter has a `lesson.md`, and its steps are folders with a `lesson.json` and a `lesson.md`.
- `samples\` holds the sample data, the sample packages, and the run folders the runner uses.
- `lesson-runner\` is the runner: a desktop window built with Electron.
- `resources\` holds the design notes for this tutorial, and it isn't published.
- `requirements.txt` lists the Python packages for the learner.

---

*Working With Data Formats is a standalone tutorial. It needs no other tutorial in this collection first.*
