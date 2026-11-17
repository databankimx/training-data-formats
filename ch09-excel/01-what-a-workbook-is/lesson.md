# What a Workbook Is

An `.xlsx` file is an OpenXML package: a zip archive, as Chapter 2 showed, with XML files inside. The parts you'll meet are the workbook, which lists the sheets, one XML file for each sheet with its cells, a table of shared strings where text is stored once, and a styles part that holds the display formats. A program that reads a workbook is reading those parts, and the library does the unzipping and the XML for you.

A sheet is a grid of cells, and each cell has an address such as `B2`. A cell holds one of a few kinds of value: text, a number, a boolean, an error, or a formula. The kind is stored, not guessed. That's the important difference from CSV, where every value is text until a reader decides otherwise. In `customers.xlsx`, the identifier is a number, the balance is a number, and the active flag is a boolean, and a library that reads the cell reports the stored kind.

A formula cell holds two things: the formula, and the value it last calculated. A program that reads the value gets the cached result, and a program that reads the formula gets the expression. Both are useful, and they can disagree if the file was saved by a tool that didn't recalculate.

The display format is the layer that most often misleads. A cell can store `980.1` and display `980.10`, or store `4410` and display it with a thousands separator. The format is a rule for showing the value, and it is kept in the styles part. A program that reads the cell gets the stored number, and the two decimal places in Excel's window are not in the file's data. The balance `0` in the screenshot is stored as the number zero, and the display rounded it.

The legacy `.xls` format is different. It's a binary container built on the OLE2 signature from Chapter 2, with records for each cell rather than XML. It holds the same kinds of value, but a reader needs a library that knows the binary records, and not every library reads it. The fifth sample in this chapter reads one.

> **Aside: the workbook is the data and the layout.**
> A workbook mixes the data with its presentation, including colours, column widths, and display formats. A program that wants only the data should read the cell values and ignore the rest, and should never treat the display as the value.

> **Common mistake.** Reading a balance cell as text because the screen shows the number with formatting. A library that returns the stored number is right, and a library that returns the formatted text is returning the wrong thing for arithmetic.

---
