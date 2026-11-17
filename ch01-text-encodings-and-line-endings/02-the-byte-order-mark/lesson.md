# The Byte-Order Mark

Some programs write a three-byte signature at the start of a UTF-8 file: `EF BB BF`. It's called the byte-order mark, or BOM. It has no visible shape. The name suggests the mark records a byte order, but in UTF-8 it only identifies the file, as a later section explains. Many editors and spreadsheet exports still write it, and many readers still don't expect it.

The trouble is the first thing a reader sees. The BOM is not part of the first column name, but a reader that doesn't skip it will treat it as the first character of the name. The header then reads as something that looks like `customer_id` and is not equal to it, so a lookup by name fails, and the error doesn't say why.

The sample below writes the start of a customer file, with its BOM, into the code, and prints the first six bytes. The BOM is the first three, and the header name follows.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// Inline data, not from a sample file. A byte-order mark (U+FEFF) followed by "customer_id", as an editor might save it.
var text = "\ufeffcustomer_id";
var bytes = System.Text.Encoding.UTF8.GetBytes(text);
Console.WriteLine(string.Join(" ", bytes.Take(6).Select(b => b.ToString("X2"))));
```
```python
# Inline data, not from a sample file. A byte-order mark (U+FEFF) followed by "customer_id", as an editor might save it.
text = "\ufeffcustomer_id"
data = text.encode("utf-8")
print(" ".join(f"{b:02X}" for b in data[:6]))
```
```javascript
// Inline data, not from a sample file. A byte-order mark (U+FEFF) followed by "customer_id", as an editor might save it.
const text = "\ufeffcustomer_id";
const bytes = new TextEncoder().encode(text);
console.log([...bytes].slice(0, 6).map((b) => b.toString(16).toUpperCase().padStart(2, "0")).join(" "));
```
~~~

The output is the same in every language:

~~~text
EF BB BF 63 75 73
~~~

The first three bytes are the BOM. The next three, `63 75 73`, are the letters `c`, `u`, and `s`. Nothing in the output looks wrong when you print the text, because the BOM has no width on screen. Only the bytes show it.

Notice that the BOM is written by some writers, not by the encoding itself. `TextEncoder` in JavaScript, `Encoding.UTF8.GetBytes` in C#, and `encode("utf-8")` in Python all leave it out. A `StreamWriter` in C# writes it by default when it's given `Encoding.UTF8`, and Python writes it only when asked for `utf-8-sig`. An editor that saves with a BOM does the same. The file does not record which choice was made.

## Big-endian and little-endian

A value that takes more than one byte has to be stored in some order. Big-endian stores the most significant byte first, the way we write numbers: in the decimal number 1234, the 1 comes first. Little-endian stores the least significant byte first. Take the four-byte number 0x12345678. Big-endian stores it as `12 34 56 78`, and little-endian stores it as `78 56 34 12`. Most processors you'll meet, including the x86 and x64 chips in ordinary computers, are little-endian. Many network protocols and file formats are big-endian, so each format has to state its order.

The byte-order mark exists to tell a reader which order a UTF-16 file uses. UTF-16 stores each character in two bytes, and the mark is the character U+FEFF. Written big-endian, it's `FE FF`. Written little-endian, it's `FF FE`. A reader that finds `FF FE` at the start knows the file is little-endian, and one that finds `FE FF` knows it's big-endian.

UTF-8 has no byte order. A byte is a byte, so there's nothing to state. The three bytes `EF BB BF` are the same U+FEFF character written in UTF-8, so the mark still appears, but it tells the reader nothing about order. It identifies the file as UTF-8 and nothing more. That's why the name "byte-order mark" is misleading for UTF-8 files.

The sample below writes the same mark in both byte orders of UTF-16. The output shows the two patterns that a reader checks.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// Inline data, not from a sample file. The byte-order mark character, written in each byte order of UTF-16.
var text = "\ufeff";
var bigBytes = System.Text.Encoding.BigEndianUnicode.GetBytes(text);
var littleBytes = System.Text.Encoding.Unicode.GetBytes(text);
var bigText = string.Join(" ", bigBytes.Select(b => b.ToString("X2")));
var littleText = string.Join(" ", littleBytes.Select(b => b.ToString("X2")));
Console.WriteLine($"big-endian: {bigText}");
Console.WriteLine($"little-endian: {littleText}");
```
```python
# Inline data, not from a sample file. The byte-order mark character, written in each byte order of UTF-16.
text = "\ufeff"
big = " ".join(f"{b:02X}" for b in text.encode("utf-16-be"))
little = " ".join(f"{b:02X}" for b in text.encode("utf-16-le"))
print(f"big-endian: {big}")
print(f"little-endian: {little}")
```
```javascript
// Inline data, not from a sample file. The byte-order mark character, written in each byte order of UTF-16.
const text = "\ufeff";
const little = Buffer.from(text, "utf16le");
const big = Buffer.from(text, "utf16le").swap16();
const hex = (buffer) => [...buffer].map((b) => b.toString(16).toUpperCase().padStart(2, "0")).join(" ");
console.log(`big-endian: ${hex(big)}`);
console.log(`little-endian: ${hex(little)}`);
```
~~~

The output is the same in every language:

~~~text
big-endian: FE FF
little-endian: FF FE
~~~

`Buffer.swap16` in JavaScript reverses each pair of bytes, which turns the little-endian form into the big-endian one. The UTF-8 mark never needs that step, because UTF-8 has no order to reverse.

> **Aside: why the order matters for text.**
> A UTF-16 file read with the wrong order doesn't fail. Each character comes out as a different character, often one from a language nobody meant to write. This is the same silent failure as the wrong encoding in the previous step, and it's why UTF-16 files carry the mark.

> **Aside: the BOM is still in the file.**
> A reader that decodes the file as UTF-8 keeps the BOM as a character, U+FEFF, at the start of the text. Some readers strip it, and some do not. The next homework item checks for it directly.

> **Common mistake.** Looking up a column called `customer_id` in a header read from a file with a BOM. The lookup finds nothing, because the name in memory is `\ufeffcustomer_id`, which looks the same on screen.

---
