# Signatures as Bytes

A signature is only bytes. Nothing in the bytes says "Parquet" until a program agrees what they mean. The sample below writes out the four signatures from the table in the last step, and prints each one in hexadecimal, so you can see the bytes a detector compares.

The signatures are typed into the code, so they are inline data. The comment marks them.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// Inline data, not from a sample file. The signatures of four formats, written as the characters a detector compares.
var signatures = new (string Kind, string Text)[]
{
    ("parquet", "PAR1"),
    ("zip", "PK\u0003\u0004"),
    ("ole2", "\u00d0\u00cf\u0011\u00e0\u00a1\u00b1\u001a\u00e1"),
    ("xml", "<?xml"),
    ("json", "["),
};
foreach (var (kind, text) in signatures)
{
    var bytes = System.Text.Encoding.Latin1.GetBytes(text);
    var hex = string.Join(" ", bytes.Select(b => b.ToString("X2")));
    Console.WriteLine($"{kind}: {hex}");
}
```
```python
# Inline data, not from a sample file. The signatures of four formats, written as the characters a detector compares.
signatures = [
    ("parquet", "PAR1"),
    ("zip", "PK\x03\x04"),
    ("ole2", "\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"),
    ("xml", "<?xml"),
    ("json", "["),
]
for kind, text in signatures:
    hex_bytes = " ".join(f"{b:02X}" for b in text.encode("latin-1"))
    print(f"{kind}: {hex_bytes}")
```
```javascript
// Inline data, not from a sample file. The signatures of four formats, written as the characters a detector compares.
const signatures = [
  ["parquet", "PAR1"],
  ["zip", "PK\x03\x04"],
  ["ole2", "\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"],
  ["xml", "<?xml"],
  ["json", "["],
];
for (const [kind, text] of signatures) {
  const hex = [...Buffer.from(text, "latin1")].map((b) => b.toString(16).toUpperCase().padStart(2, "0")).join(" ");
  console.log(`${kind}: ${hex}`);
}
```
~~~

The output is the same in every language:

~~~text
parquet: 50 41 52 31
zip: 50 4B 03 04
ole2: D0 CF 11 E0 A1 B1 1A E1
xml: 3C 3F 78 6D 6C
json: 5B
~~~

Each line is what a detector compares, byte for byte, with the first bytes of a file. The Parquet line is `50 41 52 31`, which is the ASCII letters `P`, `A`, `R`, and `1`. The zip line is the start of a local file header, and an `.xlsx` workbook starts with one, since it is a zip archive of XML files. The JSON line is the single bracket, which is why the detector also skips any whitespace before it.

The samples use Latin-1 for these bytes, and that choice matters for the OLE2 line. Latin-1 maps each byte to the character with the same value, so the bytes come out exactly as written. Most signature bytes are below 128, where UTF-8 would give the same result. The OLE2 bytes are above 127, and UTF-8 would turn each of them into two bytes. The lesson is the same as before: a signature is a byte-level test, so compare bytes, not text.

> **Aside: the zip signature is not an Excel signature.**
> A detector that finds `50 4B 03 04` knows it has a zip archive. Whether that archive is a workbook needs a look inside, at the file list. The sample files in this chapter use the zip result, and the homework leaves the workbook question alone.

> **Common mistake.** Comparing a signature with a string in your language, rather than with the bytes. A string comparison can succeed or fail depending on the encoding that decoded the file, while the bytes are the same either way.

---
