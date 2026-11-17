# Summary: Text, Encodings, and Line Endings

This chapter covered how a file's bytes become characters, and the three things that go wrong quietly when the agreement is not kept.

## What you learned

- A file stores bytes. Only an agreed encoding turns them into characters, and the file doesn't record which encoding was used.
- In UTF-8, the length of a string in characters is not its length in bytes. An accented letter takes two bytes.
- A UTF-8 byte-order mark, `EF BB BF`, may start a file. A reader that doesn't expect it keeps it as part of the first name.
- A Windows-1252 file read as UTF-8 doesn't raise an error. Each byte that isn't valid UTF-8 becomes a replacement character, and the line count stays right.
- Some readers translate CRLF into LF without telling you. Read the raw bytes when the endings matter, and count the CRLF pairs and the LF bytes separately.
- The right fix depends on what the file is. Check the encoding and the mark before you trust the text.

## Quizzes

Three questions, one for each big idea in the chapter. Pick an answer, and read the explanation whichever way it goes.

```quiz
A UTF-8 reader meets the byte E9 in a Windows-1252 file, where the letter should be é. What happens?
○ An error is raised, and the program stops.
→ Most readers in lenient mode don't stop. They substitute, which is why the problem is easy to miss.
◉ The byte becomes the replacement character, U+FFFD, and the program carries on.
→ Right. The line count and the rest of the text stay correct, so only the accented letter shows the damage.
○ The byte is read as é, because E9 is always that letter.
→ E9 is é in Windows-1252, but UTF-8 reads it differently. The meaning depends on the encoding the reader assumed.
```

```quiz
A file starts with the bytes EF BB BF. What is that?
○ A line ending, written at the top of the file by a Windows editor.
→ Line endings are LF or CRLF, and they come at the end of each line, not the start.
○ The first customer's identifier, written in hexadecimal.
→ The identifier would be text, and these bytes do not spell out a readable number.
◉ A UTF-8 byte-order mark, which some writers add at the start of a file.
→ Right. It has no width on screen, so a reader that doesn't expect it keeps it as part of the first name.
```

```quiz
A file's line count looks correct in your editor, but the file may mix CRLF and LF. Which check shows the mix?
◉ Counting the CRLF pairs and the LF bytes in the raw data.
→ Right. The raw bytes keep the difference that text mode would hide.
○ Counting the lines in text mode, after the reader has opened the file.
→ Text mode translates CRLF into LF, so the mix disappears before you count.
○ Opening the file in the editor and looking at the line breaks.
→ Editors often convert line endings on open, so the display can hide the mix on disk.
```

---
