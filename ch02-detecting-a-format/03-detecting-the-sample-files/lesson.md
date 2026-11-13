# Detecting the Sample Files

Now the rules run on real files. The sample reads each file's bytes from the sample data folder and prints the kind the detector gives. The checks run in order from the first step: Parquet, zip, OLE2, JSON, XML, then binary or text.

The names of the files to check are typed into the code, which makes them inline data. The files themselves are read from `TRAINING_DATA`.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// Inline data, not from a sample file. The names of the files to check, in the order they are printed.
var names = new[]
{
    "customers.csv",
    "customers.json",
    "customers.jsonl",
    "customers.xml",
    "customers.xlsx",
    "customers.xls",
    "customers.parquet",
    "customers-as-json.csv",
    "customers-utf8-bom.csv",
    "customers-truncated.json",
    "config-norway.yaml",
};
var folder = Environment.GetEnvironmentVariable("TRAINING_DATA");
foreach (var name in names)
{
    var data = File.ReadAllBytes(Path.Combine(folder, name));
    Console.WriteLine($"{name}: {Kind(data)}");
}

// Checks the signatures in order, and returns the first kind that matches.
string Kind(byte[] data)
{
    if (StartsWith(data, "PAR1")) return "parquet";
    if (StartsWith(data, "PK\u0003\u0004")) return "zip";
    if (StartsWith(data, "\u00d0\u00cf\u0011\u00e0\u00a1\u00b1\u001a\u00e1")) return "ole2";
    var start = 0;
    while (start < data.Length && (data[start] == (byte)' ' || data[start] == (byte)'\t' || data[start] == (byte)'\r' || data[start] == (byte)'\n'))
    {
        start++;
    }
    if (start < data.Length && (data[start] == (byte)'[' || data[start] == (byte)'{')) return "json";
    if (StartsWith(data, "<?xml")) return "xml";
    if (Array.IndexOf(data, (byte)0) >= 0) return "binary";
    return "text";
}

bool StartsWith(byte[] data, string text)
{
    if (data.Length < text.Length) return false;
    for (var i = 0; i < text.Length; i++)
    {
        if (data[i] != (byte)text[i]) return false;
    }
    return true;
}
```
```python
import os

# Inline data, not from a sample file. The names of the files to check, in the order they are printed.
names = [
    "customers.csv",
    "customers.json",
    "customers.jsonl",
    "customers.xml",
    "customers.xlsx",
    "customers.xls",
    "customers.parquet",
    "customers-as-json.csv",
    "customers-utf8-bom.csv",
    "customers-truncated.json",
    "config-norway.yaml",
]


def kind_of(data: bytes) -> str:
    # Checks the signatures in order, and returns the first kind that matches.
    if data.startswith(b"PAR1"):
        return "parquet"
    if data.startswith(b"PK\x03\x04"):
        return "zip"
    if data.startswith(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"):
        return "ole2"
    if data.lstrip(b" \t\r\n")[:1] in (b"[", b"{"):
        return "json"
    if data.startswith(b"<?xml"):
        return "xml"
    if b"\x00" in data:
        return "binary"
    return "text"


for name in names:
    with open(os.path.join(os.environ["TRAINING_DATA"], name), "rb") as handle:
        print(f"{name}: {kind_of(handle.read())}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";

// Inline data, not from a sample file. The names of the files to check, in the order they are printed.
const names = [
  "customers.csv",
  "customers.json",
  "customers.jsonl",
  "customers.xml",
  "customers.xlsx",
  "customers.xls",
  "customers.parquet",
  "customers-as-json.csv",
  "customers-utf8-bom.csv",
  "customers-truncated.json",
  "config-norway.yaml",
];

// Checks the signatures in order, and returns the first kind that matches.
function kindOf(data) {
  const starts = (text) => data.subarray(0, text.length).equals(Buffer.from(text, "latin1"));
  if (starts("PAR1")) return "parquet";
  if (starts("PK\x03\x04")) return "zip";
  if (starts("\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1")) return "ole2";
  const first = data.toString("latin1").replace(/^[ \t\r\n]+/, "")[0];
  if (first === "[" || first === "{") return "json";
  if (starts("<?xml")) return "xml";
  if (data.includes(0)) return "binary";
  return "text";
}

for (const name of names) {
  const data = readFileSync(path.join(process.env.TRAINING_DATA, name));
  console.log(`${name}: ${kindOf(data)}`);
}
```
~~~

The output is the same in every language:

~~~text
customers.csv: text
customers.json: json
customers.jsonl: json
customers.xml: xml
customers.xlsx: zip
customers.xls: ole2
customers.parquet: parquet
customers-as-json.csv: json
customers-utf8-bom.csv: text
customers-truncated.json: json
config-norway.yaml: text
~~~

Read the output against the file names. `customers.xlsx` is reported as a zip, not a workbook, for the reason in the second step. `customers.xls` is the legacy binary workbook, and it's reported as OLE2, the container it uses. Like `customers.xlsx`, the detector can't say it holds a workbook from the first bytes alone. `customers-as-json.csv` is reported as JSON, although its name says CSV, and the next sample looks at it more closely. `customers-truncated.json` is reported as JSON, because the start is intact. The detector says what the file is, not whether it is whole.

`customers-utf8-bom.csv` is reported as text. The byte-order mark isn't a signature that changes the kind, so the detector looks past it, and the homework returns to it.

> **Aside: the order matters for JSON and text.**
> If the text rule ran before the JSON rule, every JSON file would be reported as text, because JSON is text too. The broad rule goes last.

> **Common mistake.** Reporting `customers.jsonl` as plain JSON and stopping there. JSON Lines starts the same way, with one object per line. A detector that needs to tell them apart reads the second line too, and the Chapter 4 lessons on JSON Lines show how.

---
