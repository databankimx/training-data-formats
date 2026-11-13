# 1. Text, Encodings, and Line Endings

A file is a sequence of bytes. A program reads those bytes as characters only after it has agreed on how the bytes map to characters, and nothing in the file says which agreement was used. Every later format rests on this step, so this chapter fixes it first. The same bytes can look like a clean list of customers in one program and like a row of question marks in another.

The chapter covers three things that go wrong quietly: the bytes a character takes in UTF-8, the byte-order mark that some editors put at the start of a file, and the line endings that a file can mix. It also covers the common case where a file is not UTF-8 at all, and a reader that assumes it is will replace characters it cannot read, without raising an error.

## Common encodings

An encoding is a rule for turning characters into bytes. The rules fall into three families, and it helps to know which family a file belongs to before you read it.

**Single-byte encodings** use one byte per character, so they hold at most 256 characters. ASCII uses only the first 128 values: English letters, digits, punctuation, and control characters such as tab and line feed. The values above 127 were left to each system, so an accented letter in a single-byte file means nothing until you know which table was used. Windows-1252 and ISO-8859-1 fill those values with western European letters. EBCDIC, used on IBM mainframes, is also single-byte, but its values are arranged differently.

**Variable-length encodings** use one to four bytes per character. UTF-8 keeps the ASCII characters at one byte and uses longer forms for the rest of Unicode. Shift_JIS, used for Japanese text, mixes one-byte and two-byte characters, so a reader has to follow the rules to find where each character ends.

**Fixed-width wide encodings** use the same number of bytes for every character. UTF-32 always uses four. UTF-16 uses two bytes for most characters and four for the rest, and it has to record the byte order, which is why it has its own byte-order mark.

Unicode is not an encoding. It's the table that gives every character a number, its code point. UTF-8, UTF-16, and UTF-32 are three ways of writing those numbers as bytes.

| Encoding | Bytes per character | What it can hold | Compatible with ASCII | Typical use |
|---|---|---|---|---|
| ASCII | 1 | 128 characters: English letters, digits, punctuation, control characters | It is the base | Old protocols, and the first half of most other encodings |
| ISO-8859-1 (Latin-1) | 1 | 256 characters: ASCII plus western European letters | Yes, the first 128 are identical | Older web pages, legacy systems |
| Windows-1252 | 1 | 256 characters: like Latin-1, with curly quotes, the euro sign, and others in the 0x80 to 0x9F range | Yes, the first 128 are identical | Windows text files, spreadsheet exports |
| UTF-8 | 1 to 4 | Every Unicode character | Yes, ASCII text is valid UTF-8 unchanged | The web, APIs, most modern files |
| UTF-16 | 2 or 4 | Every Unicode character | No | Strings inside Windows, .NET, and Java |
| UTF-32 | 4 | Every Unicode character | No | Internal processing where a fixed width helps |
| Shift_JIS | 1 or 2 | Japanese kana, kanji, and ASCII | Yes, for ASCII characters | Older Japanese files |
| EBCDIC (code page 037) | 1 | 256 characters in the IBM mainframe layout | No: the letter A is 0xC1, not 0x41 | IBM mainframe data |

Two practical points follow from the table. First, a file that contains only ASCII reads the same in every ASCII-compatible encoding, so you can't tell them apart from the bytes alone. EBCDIC and the wide encodings read the same bytes as different characters, so a guess does matter. The trouble for the ASCII-compatible ones starts with the first accented letter, and that's the case the rest of this chapter is about. Second, EBCDIC and the wide encodings need their own readers. Python names EBCDIC as `cp037`. C# needs a code-page provider for it, and the JavaScript `TextDecoder` can't read it at all.

> **Aside: code page numbers.**
> Windows names its encodings with numbers. Code page 1252 is Windows-1252, 65001 is UTF-8, and 437 is the original IBM PC character set. A number in a log or a configuration file is a quick clue to the encoding, when the file itself doesn't say.

The chapter has four reading steps, each with a sample, three homework items, and a summary with three quizzes. The samples for the first two use inline data, which the comment above each one marks. The samples for the third and fourth read sample files. The homework reads sample files, and each item fixes one of the bad files in this chapter.

**Libraries.** No third-party packages. C# uses `System.Text` (for `Encoding`), `System.IO`, and `System.Linq`, all part of the .NET base libraries. Python uses `os`, and everything else the samples need is part of the language. JavaScript uses `node:fs`, `node:path`, `TextEncoder`, `TextDecoder`, and `Buffer`, all built into Node.

---
