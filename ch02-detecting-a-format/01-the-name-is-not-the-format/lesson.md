# The Name Is Not the Format

An extension is a label that someone attached to a file. Nothing checks it. A tool that exports a report can name the file `report.csv` whatever it writes inside, and a person who renames a workbook to `.txt` to attach it to an email has changed the label, not the contents. Programs that rely on the name will try to read the file as the format the name suggests.

The reliable test is the content. Most formats begin with a few bytes that identify them. Those bytes are the file's signature, sometimes called its magic bytes. A detector reads the first bytes, compares them with the known signatures, and reports the kind of file it found. The table lists the signatures this tutorial uses.

| Kind | How it starts | Notes |
|---|---|---|
| Parquet | `PAR1`, the ASCII letters | Parquet files also end with `PAR1` |
| Zip archive, including `.xlsx` | `PK` followed by bytes `03 04` | Excel workbooks are zip archives, so the signature says zip, not Excel |
| OLE2 compound file, including legacy `.xls` | `D0 CF 11 E0 A1 B1 1A E1` | Older Office formats use this container rather than zip |
| JSON | `[` or `{`, after any whitespace | JSON Lines also starts with `{` |
| XML | `<?xml` | Some XML files have no declaration, so a missing one doesn't rule XML out |
| Text | No NUL byte, and nothing above matched | CSV, YAML, and most configuration files fall here |
| Binary | A NUL byte, and nothing above matched | Anything else that is not text |

Modern Office files, such as `.xlsx`, `.docx`, and `.pptx`, are OpenXML formats. An OpenXML file is a zip archive, and inside it are XML files: the workbook's sheets, its styles, and a list of its parts. That's why an `.xlsx` workbook is detected as a zip. The zip signature describes the container, not the application, so a zip could hold a workbook, a document, or something else. Telling them apart means looking inside the archive for the files that belong to each format, such as `xl/workbook.xml` for a workbook. That needs a zip reader, which the Excel chapter covers.

Legacy `.xls` files are a different container. Before 2007, Excel saved workbooks in a binary format built on OLE2 compound files, with its own record layout rather than XML. The OLE2 signature identifies the container, and other older Office files use the same one, so the kind it reports is legacy Office, not Excel specifically.

The order matters. A Parquet file's first four bytes are letters, so no other check can match them, but a plain text file that begins with `[` would match the JSON check. Check the most specific signatures first, and leave the broad "text" rule until last.

Detection answers one question: what kind of file is this? It doesn't answer whether the file is well formed. A JSON file cut off halfway still starts with `[`, so the detector says JSON. The parser that reads the whole file will find the truncation, and the next chapters show that. Keep the two questions apart, because a detector that claims more than it knows will send you to the wrong fix.

> **Aside: why read only the start?**
> A detector can read the first few kilobytes and stop. The signatures sit in the first few bytes, but the text-or-binary check looks further in for a NUL byte, so a few kilobytes is the usual limit. The samples in this chapter read whole files, because the sample files are small.

> **Common mistake.** Deciding a file's format from its name, then reporting a parse error as a fault in the parser. The parser was given the wrong format. Check the content first.

---
