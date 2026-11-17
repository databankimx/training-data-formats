# Characters and Bytes

A character is a letter, a digit, or a symbol. A byte is eight bits, a number from 0 to 255. A file stores bytes. A program reads bytes and decides which characters they stand for, and the rule for that decision is the encoding.

The most common encoding is UTF-8. In UTF-8, the letters of plain English take one byte each, and other characters take more. The letter `e` is one byte. The letter `é`, with its accent, is two bytes. The file on disk doesn't say which rule was used, so a reader must already know it.

The sample below types one accented letter into the code and prints its UTF-8 bytes, in hexadecimal. The letter is given as an escape, `\u00e9`, so you can see its code point without relying on your editor.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// Inline data, not from a sample file. One accented letter, given by its code point, so the lesson shows its bytes exactly.
var text = "\u00e9";
var bytes = System.Text.Encoding.UTF8.GetBytes(text);
Console.WriteLine(string.Join(" ", bytes.Select(b => b.ToString("X2"))));
```
```python
# Inline data, not from a sample file. One accented letter, given by its code point, so the lesson shows its bytes exactly.
text = "\u00e9"
data = text.encode("utf-8")
print(" ".join(f"{b:02X}" for b in data))
```
```javascript
// Inline data, not from a sample file. One accented letter, given by its code point, so the lesson shows its bytes exactly.
const text = "\u00e9";
const bytes = new TextEncoder().encode(text);
console.log([...bytes].map((b) => b.toString(16).toUpperCase().padStart(2, "0")).join(" "));
```
~~~

The output is the same in every language:

~~~text
C3 A9
~~~

Two bytes, `C3` and `A9`, make one letter. Change the code to `"e"` and the output becomes a single byte, `65`. Try it in each tab. The length of a string in characters, and the length of its encoded form in bytes, are different numbers, and a program that confuses them will cut a value in the wrong place.

> **Aside: the code point.**
> Each character has a number, its code point. The accented e is U+00E9. UTF-8 is one way of turning that number into bytes. Other encodings turn the same number into different bytes, which is the reason for the rest of this chapter.

> **Common mistake.** Using the length of a string to decide how many bytes to read. Length counts characters. A reader that expects one byte per character will misread any file with accents, and will do so without an error.

---
