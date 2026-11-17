# JSON Lines to XML

This link reads `customers.jsonl` and writes `customers.xml`. The change in form is the important part. A JSON object's keys become element names, and the identifier becomes an attribute on the `customer` element, because it is an identifier rather than content. The address stays nested, because XML can hold a nested element as easily as JSON holds an object. The tags are the one change in shape: a JSON list becomes repeated `tag` elements inside a `tags` element.

An empty list is written as an empty `tags` element. The next link treats a missing or empty `tags` element as an empty list, so a customer with no tags comes through the loop unchanged.

The output is the number of records written.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// The lines are read from the chain folder, and the customers are written as XML there for the next link to read.
using System.Text.Json;
using System.Xml.Linq;
var source = Path.Combine(Environment.GetEnvironmentVariable("CHAIN_DATA"), "customers.jsonl");
var target = Path.Combine(Environment.GetEnvironmentVariable("CHAIN_DATA"), "customers.xml");
var root = new XElement("customers");
var count = 0;
foreach (var line in File.ReadLines(source, System.Text.Encoding.UTF8))
{
    using var record = JsonDocument.Parse(line);
    var json = record.RootElement;
    var address = json.GetProperty("address");
    var tags = new XElement("tags");
    foreach (var tag in json.GetProperty("tags").EnumerateArray())
    {
        tags.Add(new XElement("tag", tag.GetString()));
    }
    root.Add(new XElement("customer",
        new XAttribute("id", json.GetProperty("customer_id").GetInt32()),
        new XElement("name", json.GetProperty("name").GetString()),
        new XElement("email", json.GetProperty("email").GetString()),
        new XElement("signup_date", json.GetProperty("signup_date").GetString()),
        new XElement("balance", json.GetProperty("balance").GetString()),
        new XElement("active", json.GetProperty("active").GetBoolean() ? "true" : "false"),
        new XElement("country_code", json.GetProperty("country_code").GetString()),
        new XElement("address",
            new XElement("street", address.GetProperty("street").GetString()),
            new XElement("city", address.GetProperty("city").GetString()),
            new XElement("postal_code", address.GetProperty("postal_code").GetString())),
        tags));
    count++;
}
new XDocument(new XDeclaration("1.0", "UTF-8", null), root).Save(target);
Console.WriteLine($"Records written: {count}");
```
```python
import json
import os

from lxml import etree

# The lines are read from the chain folder, and the customers are written as XML there for the next link to read.
source = os.path.join(os.environ["CHAIN_DATA"], "customers.jsonl")
target = os.path.join(os.environ["CHAIN_DATA"], "customers.xml")
root = etree.Element("customers")
count = 0
with open(source, encoding="utf-8") as handle:
    for line in handle:
        record = json.loads(line)
        customer = etree.SubElement(root, "customer", id=str(record["customer_id"]))
        etree.SubElement(customer, "name").text = record["name"]
        etree.SubElement(customer, "email").text = record["email"]
        etree.SubElement(customer, "signup_date").text = record["signup_date"]
        etree.SubElement(customer, "balance").text = record["balance"]
        etree.SubElement(customer, "active").text = "true" if record["active"] else "false"
        etree.SubElement(customer, "country_code").text = record["country_code"]
        address = etree.SubElement(customer, "address")
        etree.SubElement(address, "street").text = record["address"]["street"]
        etree.SubElement(address, "city").text = record["address"]["city"]
        etree.SubElement(address, "postal_code").text = record["address"]["postal_code"]
        tags = etree.SubElement(customer, "tags")
        for tag in record["tags"]:
            etree.SubElement(tags, "tag").text = tag
        count += 1
etree.ElementTree(root).write(target, xml_declaration=True, encoding="UTF-8", pretty_print=True)
print(f"Records written: {count}")
```
```javascript
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { XMLBuilder } from "fast-xml-parser";

// The lines are read from the chain folder, and the customers are written as XML there for the next link to read.
const records = readFileSync(path.join(process.env.CHAIN_DATA, "customers.jsonl"), "utf8")
  .split("\n")
  .filter((line) => line !== "")
  .map((line) => JSON.parse(line));
const customers = records.map((record) => ({
  "@_id": record.customer_id,
  name: record.name,
  email: record.email,
  signup_date: record.signup_date,
  balance: record.balance,
  active: record.active ? "true" : "false",
  country_code: record.country_code,
  address: {
    street: record.address.street,
    city: record.address.city,
    postal_code: record.address.postal_code,
  },
  tags: { tag: record.tags },
}));
const builder = new XMLBuilder({ ignoreAttributes: false, attributeNamePrefix: "@_", format: true, indentBy: "  " });
writeFileSync(path.join(process.env.CHAIN_DATA, "customers.xml"), builder.build({ customers: { customer: customers } }), "utf8");
console.log(`Records written: ${records.length}`);
```
~~~

The output is the same in every language:

~~~text
Records written: 12
~~~

The XML has the same values as the JSON Lines it came from. The identifier is an attribute, and the balance is still text, so `0.00` is written as `0.00` and not as a number. The element order follows the field order in the code, and the customers appear in the order they were read.

> **Aside: attributes and elements are a choice.**
> The identifier could have been an element, and a reader that expects the other form would fail. This link chooses attributes for the identifier and elements for everything else, and the next link reads the same choice back.

> **Common mistake.** Writing an empty list as nothing at all. A reader that expects a `tags` element then finds none and fails, or treats the absence as missing data. Write the empty element, and read a missing one as an empty list.

---
