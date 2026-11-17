# Reading XML

Reading XML means parsing the whole document into a tree, then walking it. Each language gives you a way to find elements by name, read an attribute, and read a child's text. The parser has to be set up before it reads anything, so the first part of each sample is the setting that refuses external references.

The sample below reads `customers.xml`, counts the customers, and prints the first one: its identifier from the `id` attribute, and its name and city from child elements. The city is nested inside `address`, so the lookup goes down two levels.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// The sample file is read from the folder named by TRAINING_DATA. DTDs are refused, so no entity is expanded.
using System.Xml;
using System.Xml.Linq;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers.xml");
var settings = new XmlReaderSettings { DtdProcessing = DtdProcessing.Prohibit, XmlResolver = null };
using var reader = XmlReader.Create(path, settings);
var root = XDocument.Load(reader).Root;
var customers = root.Elements("customer").ToList();
var first = customers[0];
var id = first.Attribute("id").Value;
var name = first.Element("name").Value;
var city = first.Element("address").Element("city").Value;
Console.WriteLine($"Customers: {customers.Count}");
Console.WriteLine($"First customer: {id} {name} {city}");
```
```python
import os

from lxml import etree

# The sample file is read from the folder named by TRAINING_DATA. External entities are not resolved, and no network access is allowed.
path = os.path.join(os.environ["TRAINING_DATA"], "customers.xml")
parser = etree.XMLParser(resolve_entities=False, no_network=True)
root = etree.parse(path, parser).getroot()
customers = root.findall("customer")
first = customers[0]
customer_id = first.get("id")
name = first.findtext("name")
city = first.find("address/city").text
print(f"Customers: {len(customers)}")
print(f"First customer: {customer_id} {name} {city}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";
import { XMLParser } from "fast-xml-parser";

// The sample file is read from the folder named by TRAINING_DATA. Attributes are kept, and their names carry the @_ prefix.
const parser = new XMLParser({ ignoreAttributes: false, attributeNamePrefix: "@_" });
const document = parser.parse(readFileSync(path.join(process.env.TRAINING_DATA, "customers.xml"), "utf8"));
const customers = document.customers.customer;
const first = customers[0];
console.log(`Customers: ${customers.length}`);
console.log(`First customer: ${first["@_id"]} ${first.name} ${first.address.city}`);
```
~~~

The output is the same in every language:

~~~text
Customers: 12
First customer: 1001 Alice Carter Springfield
~~~

Each sample reaches the same three values by a different route. C# walks the tree with `Elements` and `Element`, and it reads attributes with `Attribute`. Python uses `findall` and `find`, with a path such as `address/city`. JavaScript reads the parsed object, where the attribute appears as `@_id` and each child is a property. The tree is the same in all three, so the values match.

The settings are the important part of the C# and Python samples. The C# reader prohibits DTDs and clears the resolver, so a DOCTYPE with an entity is refused before anything is expanded. The Python parser has `resolve_entities=False`, which leaves an entity reference unresolved, and `no_network=True`, which stops it fetching a URL. As the next step's sample shows, `no_network` alone is not enough to stop a local file being read, so both settings are needed.

The JavaScript parser's behaviour with external entities is set by its own options, and the samples here don't declare any, so the entity sample will show what that parser does with one.

> **Aside: the parser builds the whole tree.**
> All three samples read the entire document into memory before returning. A very large XML file needs a streaming reader, which this tutorial doesn't cover, and the libraries' documentation describes it.

> **Common mistake.** Searching the text for `<customer ` to count customers. A comment or a string inside an attribute can contain the same characters. Walk the tree.

---
