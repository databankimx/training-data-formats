# Writing XML

Writing XML means producing a tree and serializing it. Each element is written with its name and attributes, then its text and children, then its closing tag. The part most often done wrong is the text. A value containing `&`, `<`, or `>` would break the markup if written as it is, and the writer has to escape it. An ampersand becomes `&amp;`, and a less-than sign becomes `&lt;`.

The sample below builds one order, with an `id` attribute and a `note` child whose text contains an ampersand. The note is typed into the code, so the data is inline, and the comment says so. The library writes the tree, and the output shows the escaped text.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// Inline data, not from a sample file. An order with an attribute and a note whose text contains an ampersand.
using System.Xml.Linq;
var order = new XElement("order", new XAttribute("id", "5001"), new XElement("note", "Tom & Jerry"));
Console.WriteLine(order.ToString());
```
```python
from lxml import etree

# Inline data, not from a sample file. An order with an attribute and a note whose text contains an ampersand.
order = etree.Element("order", id="5001")
note = etree.SubElement(order, "note")
note.text = "Tom & Jerry"
print(etree.tostring(order, pretty_print=True).decode())
```
```javascript
import { XMLBuilder } from "fast-xml-parser";

// Inline data, not from a sample file. An order with an attribute and a note whose text contains an ampersand.
const builder = new XMLBuilder({ ignoreAttributes: false, attributeNamePrefix: "@_", format: true, indentBy: "  " });
console.log(builder.build({ order: { "@_id": "5001", note: "Tom & Jerry" } }));
```
~~~

The output is the same in every language:

~~~text
<order id="5001">
  <note>Tom &amp; Jerry</note>
</order>
~~~

The ampersand in the note is written as `&amp;`, so a reader gets back the original text. Nothing in the program wrote that escape by hand. The attribute is written in quotes, and the element is closed in the right order. The library did each of those things, and the sample only said what the tree contained.

The escape is needed in attributes as well as text. An attribute value containing a double quote has to be escaped too, and every library does that when it's given the value. A string built by hand, with quotes and angle brackets joined in, does not get the escapes right the first time.

> **Aside: the output is a tree, not a string.**
> Each library builds the tree first and serializes it second, so the structure is correct before any text is written. That's why an unclosed tag can't appear in the output: the tree has no unclosed nodes.

> **Common mistake.** Writing `<note>` followed by the text and `</note>`, with the text pasted in. A note reading `Tom & Jerry` produces invalid XML, and a parser stops at the ampersand. Escape the text, or let the library do it.

---
