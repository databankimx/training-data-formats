# Line Endings

A line ending is one or two bytes that mark the end of a line. Unix tools and most modern programs use LF, which is the single byte `0A`. Windows tools traditionally use CRLF, which is two bytes, `0D 0A`: a carriage return followed by a line feed. Both are valid, and both are common, so a file can contain either or both.

Most readers hide the difference. A reader in text mode turns CRLF into LF, and the program sees only lines. That's convenient until the file is one you need to check, or to write back unchanged. A file that mixes the two endings will look fine in most editors, and a tool that counts lines by LF will count correctly, but a tool that compares bytes will see two kinds of line.

The sample file `customers-mixed-line-endings.csv` alternates between the two endings. The sample below decodes the file as UTF-8, splits it at each LF, and prints the first three lines. Each line is followed by its ending, shown as `[LF]` or `[CRLF]`. The decoded text keeps the carriage return, so the difference is visible in the output.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// The sample file is read from the folder named by TRAINING_DATA. It is decoded as UTF-8, and the carriage returns stay in the text.
var folder = Environment.GetEnvironmentVariable("TRAINING_DATA");
var bytes = File.ReadAllBytes(Path.Combine(folder, "customers-mixed-line-endings.csv"));
var lines = System.Text.Encoding.UTF8.GetString(bytes).Split('\n');
for (var number = 1; number <= 3; number++)
{
    var line = lines[number - 1];
    var ending = line.EndsWith('\r') ? "CRLF" : "LF";
    Console.WriteLine($"{number}: {line.TrimEnd('\r')} [{ending}]");
}
```
```python
import os

# The sample file is read from the folder named by TRAINING_DATA. It is decoded as UTF-8, and the carriage returns stay in the text.
path = os.path.join(os.environ["TRAINING_DATA"], "customers-mixed-line-endings.csv")
with open(path, "rb") as handle:
    lines = handle.read().decode("utf-8").split("\n")
for number, line in enumerate(lines[:3], start=1):
    ending = "CRLF" if line.endswith("\r") else "LF"
    print(f"{number}: {line.rstrip(chr(13))} [{ending}]")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";

// The sample file is read from the folder named by TRAINING_DATA. It is decoded as UTF-8, and the carriage returns stay in the text.
const bytes = readFileSync(path.join(process.env.TRAINING_DATA, "customers-mixed-line-endings.csv"));
const lines = bytes.toString("utf8").split("\n");
for (let number = 1; number <= 3; number++) {
  const line = lines[number - 1];
  const ending = line.endsWith("\r") ? "CRLF" : "LF";
  console.log(`${number}: ${line.replace(/\r$/, "")} [${ending}]`);
}
```
~~~

The output is the same in every language:

~~~text
1: customer_id,name,email,signup_date,balance,active,country_code,address_street,address_city,address_postal_code,tags [LF]
2: 1001,Alice Carter,alice.carter@example.invalid,2021-03-14,1250.75,true,US,12 Maple Street,Springfield,62704,vip;newsletter [CRLF]
3: 1002,"Okafor, Chidi",chidi.okafor@example.invalid,2020-11-02,0.00,false,GB,14 Harbour Road,Bristol,BS1 4DJ, [LF]
~~~

The header ends in LF, the first customer ends in CRLF, and the next line goes back to LF. The file alternates, so every second line ends in CRLF. The generator wrote it that way on purpose. Nothing in a real file tells you the endings are mixed, and nothing about the first line tells you what the rest will be.

The sample stops at line 3. The fourth line holds an accented letter, and the output stays plain ASCII so it prints the same in every console. The encoding doesn't change the endings either. CR and LF are single bytes in UTF-8, just as they are in ASCII, so the check works on the decoded text as well as on the raw bytes.

> **Aside: why a tool might count lines differently.**
> A line counter that counts LF characters counts every line here. One that counts lines in text mode also counts every line, because text mode turns CRLF into LF. A counter that looks for CRLF alone counts only half. The next homework item counts each kind.

> **Common mistake.** Assuming a file has one line ending because it looks uniform in the editor you opened it in. Editors often convert on open, and the bytes on disk stay mixed.

---
