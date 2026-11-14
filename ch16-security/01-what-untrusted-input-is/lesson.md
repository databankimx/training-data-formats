# What Untrusted Input Is

A file can harm the program that reads it in five ways, and each needs its own defence. The first is size. A file of several gigabytes read whole into memory exhausts the machine, and a small file that expands when read, such as a compressed archive, can do the same. The defence is a limit checked before the work starts, on the size of the file and on the size of anything it expands to.

The second is structure. A document that nests thousands of levels deep, or repeats an element a million times, can exhaust a parser's stack or memory. An XML file whose entities refer to one another can expand exponentially: each level multiplies the text of the level below, and a few kilobytes of file become gigabytes of text. The defence is a limit on depth and on expansion, and, for XML, turning entity expansion off, as the XML chapter showed.

The third is reference. An entity can name a local file, and the parser reads that file into the document. The defence is to refuse external references, as the XML chapter's sample did.

The fourth is execution. A spreadsheet runs a cell that begins with `=`, and it may fetch data from elsewhere when it opens. The defence is to neutralise such cells before the file reaches a spreadsheet, or to refuse them, as the CSV and Excel chapters showed.

The fifth is the log. Anything the program writes about the input can carry the input's own text into the log. A value that contains a line break can forge a second log entry, and a value that contains a control sequence can alter what a terminal shows. The defence is to log the problem and its location, and to leave the value out.

Each defence follows one rule: decide what the input is allowed to be before the program acts on it, and refuse what does not fit. A limit checked after the file is read is not a limit on reading.

> **Aside: a limit must come before the work.**
> A check on the size of the data after it has been parsed protects nothing, because the memory is already used. Check the size of the file, or count as the data is read, and stop before the expansion.

> **Common mistake.** Treating a file as safe because it is a common format. A CSV, an XML document, and a spreadsheet are each a route into a different kind of harm, and a safe parser does not make the content safe to use.

---
