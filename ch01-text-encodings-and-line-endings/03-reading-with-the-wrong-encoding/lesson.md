# Reading with the Wrong Encoding

Windows-1252 is a single-byte encoding. Each byte is one character, and the characters it holds are the ones common in western European text, such as `é`, `ó`, and `ß`. Many exports from older systems and from spreadsheets saved on Windows use it. The sample file `customers-windows-1252.csv` is one of them.

The byte that stands for `é` in Windows-1252 is `E9`. In UTF-8, `E9` is the first byte of a three-byte sequence, and a three-byte sequence must be followed by two more bytes that continue it. The next byte in the file is `e`, which can't continue it. A UTF-8 reader therefore can't make sense of the byte, and it can't stop either, because the file is valid as far as the reader is concerned. It substitutes the replacement character, U+FFFD, and carries on.

No error is raised. The program runs, the output is the right number of lines, and every name is there. Only the accented letters are wrong, and they are wrong in a way that looks like damage rather than a mistake.

The sample below reads the file's bytes and decodes them as UTF-8. It prints each line that holds a replacement character, with the replacement shown as `<?>` so the output is plain text. Then it counts the replacements. The file has four accented letters in it, on three lines, so the count is four.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// The sample file is read from the folder named by TRAINING_DATA. It is Windows-1252, but it's decoded here as UTF-8.
var folder = Environment.GetEnvironmentVariable("TRAINING_DATA");
var bytes = File.ReadAllBytes(Path.Combine(folder, "customers-windows-1252.csv"));
var text = System.Text.Encoding.UTF8.GetString(bytes);
// Print each line that holds a replacement character, with the character shown as <?> so the output is plain text.
foreach (var line in text.Split('\n'))
{
    if (line.Contains('\uFFFD'))
    {
        Console.WriteLine(line.Replace("\uFFFD", "<?>"));
    }
}
var replacements = text.Count(c => c == '\uFFFD');
Console.WriteLine($"Replacement characters: {replacements}");
```
```python
import os

# The sample file is read from the folder named by TRAINING_DATA. It is Windows-1252, but it's decoded here as UTF-8.
path = os.path.join(os.environ["TRAINING_DATA"], "customers-windows-1252.csv")
with open(path, "rb") as handle:
    data = handle.read()
text = data.decode("utf-8", errors="replace")
# Print each line that holds a replacement character, with the character shown as <?> so the output is plain text.
for line in text.split("\n"):
    if "\ufffd" in line:
        print(line.replace("\ufffd", "<?>"))
print(f"Replacement characters: {text.count(chr(0xFFFD))}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";

// The sample file is read from the folder named by TRAINING_DATA. It is Windows-1252, but it's decoded here as UTF-8.
const bytes = readFileSync(path.join(process.env.TRAINING_DATA, "customers-windows-1252.csv"));
const text = new TextDecoder("utf-8").decode(bytes);
// Print each line that holds a replacement character, with the character shown as <?> so the output is plain text.
for (const line of text.split("\n")) {
  if (line.includes("\uFFFD")) console.log(line.replaceAll("\uFFFD", "<?>"));
}
console.log(`Replacement characters: ${text.split("\uFFFD").length - 1}`);
```
~~~

The output is the same in every language:

~~~text
1003,Ren<?>e Dubois,renee.dubois@example.invalid,2022-06-30,980.10,true,FR,7 Rue des Lilas,Lyon,69001,newsletter
1006,Samuel Osei,samuel.osei@example.invalid,2021-07-22,0.00,false,DE,Hauptstra<?>e 3,Berlin,10115,dormant
1011,Tomasz W<?>jcik,tomasz.wojcik@example.invalid,2021-12-01,640.00,true,PL,ul. Piotrkowska 10,?<?>d?,90-001,newsletter
Replacement characters: 4
~~~

The three lines are the customers with accented letters. In Renée's name, the é has become `<?>`. Samuel Osei's street, Hauptstraße, has lost its ß. Tomasz Wójcik has two replacements, one in his surname and one in his city. The city is Łódź, and the file shows it as `?ód?`. Those question marks are real. When the file was made, Windows-1252 had no letter for `Ł` or `ź`, so the writer put a question mark in their place. That's a loss in the file itself, and no reader can recover it.

> **Aside: a reader that never fails.**
> Most readers have a strict mode that refuses invalid bytes. The samples here use the lenient mode, because that is the mode that hides the problem. The XML parser in Chapter 7 refuses invalid bytes by default, which is one reason it's stricter than a plain text reader.

> **Common mistake.** Trusting the output because it has the right number of lines. The line count is correct, so the damage is easy to miss. Check the bytes, or the encoding the file was written in, before you trust the text.

---
