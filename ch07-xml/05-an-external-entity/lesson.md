# An External Entity

The file `orders-xxe.xml` declares an entity in its DOCTYPE, and the entity points at a file: `file:///example/secret-notes.txt`. The path is a reserved example and doesn't exist on any machine. The note of the first order refers to that entity by name. A parser that resolves external entities would read the file and place its contents in the note. On a real system, the file would be a password store, a configuration file, or a private key.

This step uses a single file, so the three samples can be compared directly. Each sample uses its library's default or safest setting, and the outputs differ, because the libraries make different choices about what to do with an external reference.

The sample below reads `orders-xxe.xml` and prints the note. The C# parser refuses any document with a DTD. The Python parser keeps the reference unresolved. The JavaScript parser refuses the external entity with an error, which the sample catches.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// The sample file is read from the folder named by TRAINING_DATA. A DTD is refused, so the external entity is never opened.
using System.Xml;
using System.Xml.Linq;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "orders-xxe.xml");
var settings = new XmlReaderSettings { DtdProcessing = DtdProcessing.Prohibit, XmlResolver = null };
try
{
    using var reader = XmlReader.Create(path, settings);
    var order = XDocument.Load(reader).Root.Element("order");
    Console.WriteLine($"Note text: {order.Element("note").Value}");
}
catch (XmlException)
{
    Console.WriteLine("Refused: the document has a DTD");
}
```
```python
import os

from lxml import etree

# The sample file is read from the folder named by TRAINING_DATA. External entities are not resolved, and no network access is allowed.
path = os.path.join(os.environ["TRAINING_DATA"], "orders-xxe.xml")
parser = etree.XMLParser(resolve_entities=False, no_network=True)
root = etree.parse(path, parser).getroot()
note = root.find("order/note")
print(f"Note is empty: {'yes' if not note.text else 'no'}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";
import { XMLParser } from "fast-xml-parser";

// The sample file is read from the folder named by TRAINING_DATA. The parser's default setting refuses an external entity with an error, which is caught here.
const parser = new XMLParser({ ignoreAttributes: false, attributeNamePrefix: "@_" });
try {
  const document = parser.parse(readFileSync(path.join(process.env.TRAINING_DATA, "orders-xxe.xml"), "utf8"));
  console.log(`Note text: ${document.orders.order.note}`);
} catch (error) {
  console.log("Refused: external entities are not supported");
}
```
~~~

The output differs by language. Each block below is the output of one language:

~~~text
C#:
Refused: the document has a DTD

Python:
Note is empty: yes

JavaScript:
Refused: external entities are not supported
~~~

Each output is safe, and each one is a different outcome. C# stops at the DOCTYPE, so the document is refused and nothing is read. Python accepts the document but leaves the reference unresolved, so the note has no text. JavaScript refuses the external entity by name, so the document is rejected at the point where it would have been read. In none of the three is the file opened.

The three settings are not the same, and that matters. C# says no DTDs at all, which is the strongest rule. Python says not to resolve external entities, and `no_network=True` on its own would not stop a `file://` reference. JavaScript's default refuses the external entity while still reading the rest of the document's structure. A system that needs the note's text should treat any of these three outcomes as a refusal, because a reference left in place can be expanded later by a different tool.

The JavaScript sample catches the error and prints its own fixed message, rather than the library's text. The library's message describes the cause, and a message in a log should describe what the program did about it.

> **Aside: why `no_network` is not enough.**
> A network setting blocks requests to remote hosts. A local file reference is not a network request, so a parser can still open it while believing the network is off. The defence has to name the entity behaviour directly.

> **Common mistake.** Trusting a parser because it is safe for web addresses. Test it with a reference to a local file, and check what the note contains afterwards.

---
