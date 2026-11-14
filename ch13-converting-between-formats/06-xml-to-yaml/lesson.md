# XML to YAML

This link reads `customers.xml` and writes `customers.yaml`. The XML's attribute becomes an ordinary key, `customer_id`, and the nested address stays nested. The values are read as text, and each writer decides how to quote them. A balance such as `0.00` has to stay text here, because some YAML readers would turn an unquoted `0.00` into a number, and an XML parser that converts tag values would do the same before the YAML is written.

The XML parser is therefore set to keep text. The C# and Python readers already return text, and the JavaScript reader is told not to convert values. A missing `tags` element is read as an empty list, which is the rule from the previous link.

The output is the number of records written.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package YamlDotNet@18.1.0

// The XML is read from the chain folder, and the customers are written as YAML there for the next link to read.
using System.Xml.Linq;
using YamlDotNet.Serialization;
var source = Path.Combine(Environment.GetEnvironmentVariable("CHAIN_DATA"), "customers.xml");
var target = Path.Combine(Environment.GetEnvironmentVariable("CHAIN_DATA"), "customers.yaml");
var customers = XDocument.Load(source).Root.Elements("customer").Select(customer => new Dictionary<string, object>
{
    ["customer_id"] = int.Parse(customer.Attribute("id").Value),
    ["name"] = customer.Element("name").Value,
    ["email"] = customer.Element("email").Value,
    ["signup_date"] = customer.Element("signup_date").Value,
    ["balance"] = customer.Element("balance").Value,
    ["active"] = customer.Element("active").Value == "true",
    ["country_code"] = customer.Element("country_code").Value,
    ["address"] = new Dictionary<string, object>
    {
        ["street"] = customer.Element("address").Element("street").Value,
        ["city"] = customer.Element("address").Element("city").Value,
        ["postal_code"] = customer.Element("address").Element("postal_code").Value,
    },
    ["tags"] = (customer.Element("tags")?.Elements("tag") ?? Enumerable.Empty<XElement>()).Select(tag => tag.Value).ToList(),
}).ToList();
File.WriteAllText(target, new SerializerBuilder().Build().Serialize(customers));
Console.WriteLine($"Records written: {customers.Count}");
```
```python
import os

import yaml
from lxml import etree

# The XML is read from the chain folder, and the customers are written as YAML there for the next link to read.
source = os.path.join(os.environ["CHAIN_DATA"], "customers.xml")
target = os.path.join(os.environ["CHAIN_DATA"], "customers.yaml")
root = etree.parse(source).getroot()
customers = []
for customer in root.findall("customer"):
    tags = customer.find("tags")
    customers.append({
        "customer_id": int(customer.get("id")),
        "name": customer.findtext("name"),
        "email": customer.findtext("email"),
        "signup_date": customer.findtext("signup_date"),
        "balance": customer.findtext("balance"),
        "active": customer.findtext("active") == "true",
        "country_code": customer.findtext("country_code"),
        "address": {
            "street": customer.find("address/street").text,
            "city": customer.find("address/city").text,
            "postal_code": customer.find("address/postal_code").text,
        },
        "tags": [tag.text for tag in tags.findall("tag")] if tags is not None else [],
    })
with open(target, "w", encoding="utf-8") as handle:
    yaml.safe_dump(customers, handle, sort_keys=False, allow_unicode=True)
print(f"Records written: {len(customers)}")
```
```javascript
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { XMLParser } from "fast-xml-parser";
import { dump } from "js-yaml";

// The XML is read from the chain folder, and the customers are written as YAML there for the next link to read.
// Values are kept as text, so the balance is not converted to a number.
const parser = new XMLParser({ ignoreAttributes: false, attributeNamePrefix: "@_", parseTagValue: false });
const parsed = parser.parse(readFileSync(path.join(process.env.CHAIN_DATA, "customers.xml"), "utf8"));
const customers = parsed.customers.customer.map((customer) => {
  const tags = customer.tags && customer.tags.tag !== undefined ? [].concat(customer.tags.tag) : [];
  return {
    customer_id: Number(customer["@_id"]),
    name: customer.name,
    email: customer.email,
    signup_date: customer.signup_date,
    balance: customer.balance,
    active: customer.active === "true",
    country_code: customer.country_code,
    address: {
      street: customer.address.street,
      city: customer.address.city,
      postal_code: customer.address.postal_code,
    },
    tags: tags,
  };
});
writeFileSync(path.join(process.env.CHAIN_DATA, "customers.yaml"), dump(customers), "utf8");
console.log(`Records written: ${customers.length}`);
```
~~~

The output is the same in every language:

~~~text
Records written: 12
~~~

The YAML the writers produce is different in layout, and the values are the same. Quoting differs too: some writers quote `NO` and `'0155'`, others leave a bare value that a YAML 1.2 reader keeps as text. The next links read values as text, so the difference does not change the result, and the final check compares values.

> **Aside: text in the middle, a decision at the end.**
> Keeping every value as text in the middle of the loop means no link makes a type decision for a value it doesn't own. The later links decide how each value is stored, and they do it once.

> **Common mistake.** Letting an XML parser convert values. A balance of `0.00` converted to a number becomes `0`, and the change is silent. Turn conversion off, or read the text and convert it yourself.

---
