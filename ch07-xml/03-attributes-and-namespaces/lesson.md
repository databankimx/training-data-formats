# Attributes and Namespaces

The sample files don't use namespaces, so this step uses a short document typed into the code. It's a single order element, written with a namespace prefix, `ns`, that is bound to the URI `urn:example:orders`. The element has an `id` attribute and one child, `amount`, which is also in the namespace.

The sample reads the root element, and prints its namespace URI, its local name without the prefix, its `id` attribute, and the amount. The local name is the part after the colon, and the namespace is the URI the prefix stands for.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// Inline data, not from a sample file. One namespaced order, typed into the code, with an attribute and a child element.
using System.Xml.Linq;
var xml = "<ns:order xmlns:ns=\"urn:example:orders\" id=\"5001\"><ns:amount>129.99</ns:amount></ns:order>";
var root = XElement.Parse(xml);
var ns = XNamespace.Get("urn:example:orders");
Console.WriteLine($"Namespace: {root.Name.NamespaceName}");
Console.WriteLine($"Local name: {root.Name.LocalName}");
Console.WriteLine($"Attribute id: {root.Attribute("id").Value}");
Console.WriteLine($"Amount: {root.Element(ns + "amount").Value}");
```
```python
from lxml import etree

# Inline data, not from a sample file. One namespaced order, typed into the code, with an attribute and a child element.
xml = b'<ns:order xmlns:ns="urn:example:orders" id="5001"><ns:amount>129.99</ns:amount></ns:order>'
parser = etree.XMLParser(resolve_entities=False, no_network=True)
root = etree.fromstring(xml, parser)
namespace = root.tag[1 : root.tag.index("}")]
local_name = root.tag.split("}")[1]
print(f"Namespace: {namespace}")
print(f"Local name: {local_name}")
print(f"Attribute id: {root.get('id')}")
print(f"Amount: {root.findtext('{urn:example:orders}amount')}")
```
```javascript
import { XMLParser } from "fast-xml-parser";

// Inline data, not from a sample file. One namespaced order, typed into the code, with an attribute and a child element.
const xml = '<ns:order xmlns:ns="urn:example:orders" id="5001"><ns:amount>129.99</ns:amount></ns:order>';
const parser = new XMLParser({ ignoreAttributes: false, attributeNamePrefix: "@_" });
const document = parser.parse(xml);
const rootName = Object.keys(document)[0];
const root = document[rootName];
console.log(`Namespace: ${root["@_xmlns:ns"]}`);
console.log(`Local name: ${rootName.split(":")[1]}`);
console.log(`Attribute id: ${root["@_id"]}`);
console.log(`Amount: ${root["ns:amount"]}`);
```
~~~

The output is the same in every language:

~~~text
Namespace: urn:example:orders
Local name: order
Attribute id: 5001
Amount: 129.99
~~~

The three samples reach the namespace differently. C# reads it straight from the name, Python reads it from the Clark notation `{uri}name`, and JavaScript looks up the `xmlns:ns` declaration on the element, because the parser keeps the prefix in the name. All three give the same URI, and that's the value a program should compare.

The prefix is `ns` here, and nothing in the output depends on it. If another document declared `urn:example:orders` as `o:`, every sample would still find the same element. A program that searched for `ns:order` by its text would fail on that document, so compare by namespace and local name.

The attribute `id` has no namespace. Unprefixed attributes belong to their element, not to the default namespace, so the lookup is by plain name. A common error is to put an attribute in a namespace it doesn't belong to.

> **Aside: why the prefix changes.**
> A prefix is chosen by the document's author, and it's only a shorthand. Two systems that exchange the same orders may use different prefixes, and both are correct.

> **Common mistake.** Matching `ns:order` as a string. The name the parser reports is the namespace and local name, and the prefix is decoration on top.

---
