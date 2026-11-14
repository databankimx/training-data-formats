# Glossary

Each entry gives a plain meaning and the chapter where the term first appears. The entries are in alphabetical order.

**Byte-order mark (BOM).** Three bytes at the start of a UTF-8 file that mark it as UTF-8. Some tools write them, and a parser that does not expect them may read them as part of the first column name. Chapter 1.

**CRLF and LF.** The two line endings in common use. CRLF is a carriage return followed by a line feed, used by Windows. LF is a line feed alone, used by Linux and macOS. A file that mixes them is a file with a problem. Chapter 1.

**Delimiter.** The character that separates fields in a delimited format: a comma in CSV, a tab in TSV. Chapter 5.

**Encoding.** The rule that maps bytes to characters. UTF-8 and Windows-1252 are both common, and the same bytes mean different text in each. Chapter 1.

**Expected value.** The known correct result that a test compares a program's output with. It must come from somewhere other than the program. Chapter 17.

**External entity.** A reference in an XML document to content outside it, such as a file or a network address. A parser that resolves one may read a file it should not. Chapter 7.

**Fixture.** A known input with a known result, used to test a program. Chapter 17.

**Fixed-width.** A format in which each field has a set column position, and no separator. Chapter 6.

**Flattening.** Turning a nested structure into a flat row, usually by joining the keys with dots, such as address.city. It can lose which fields belonged together. Chapter 3.

**Formula cell.** A spreadsheet cell whose text begins with =, +, -, or @, which a spreadsheet may run as a formula. Chapter 16.

**Golden-file test.** A test that compares a program's output with a stored expected output, and fails when the two differ. Chapter 17.

**Golden file.** The stored expected output that a golden-file test compares against. A change to it needs a reviewer. Chapter 17.

**Line-delimited.** A format with one record per line, such as JSON Lines. Chapter 4.

**Lossy conversion.** A conversion that changes or drops a value, so the output no longer matches the input. Chapter 13.

**Norway problem.** The YAML 1.1 behaviour that reads the unquoted country code NO as a boolean false. Chapter 8.

**Nullable.** A property or column that may hold no value. In C#, a value type such as a number must be declared nullable to hold one. Chapter 10.

**Parser.** The part of a library that turns text into values. Chapter 1.

**Refusal test.** A test that checks bad input is rejected, and that good input is accepted. Chapter 17.

**Ragged row.** A row with a different number of fields from the header. Chapter 5.

**Round-trip test.** A test that writes data out, reads it back, and checks that nothing changed. Chapter 17.

**Schema.** A description of what a valid file must contain: its fields, their types, and their rules. Chapter 11.

**Serialization.** Turning objects in a program into text or bytes that can be stored or sent. Deserialization is the reverse. Chapter 14.

**Trim.** Removing whitespace from the start and end of a value. Chapter 12.

**Validation.** Checking a file against a schema or rules, and reporting the values that fail. Chapter 11.

**Columnar.** A storage layout that keeps each column together, as Parquet does. Chapter 10.

**TRAINING_DATA.** The environment variable the runner sets to the sample data folder. A sample builds its file path from it. Chapter 0.

**CHAIN_DATA.** The environment variable the runner sets to the folder shared by the conversion links in Chapter 13. Chapter 13.

**Inline data.** Data typed into the code instead of read from a sample file. A sample that does this says so in a comment. Chapter 0.

---
