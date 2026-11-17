# 7. XML

XML is the older of the structured formats. It's a tree of elements, each with a name, optional attributes, and text or child elements, and it's still the format of choice for many enterprise integrations, configuration files, and document standards. Its power is also its risk. An XML document can declare entities, reference external files, and expand itself into something far larger than it looks, so an XML parser is a piece of software that reads instructions, not just data.

The sample files are `customers.xml`, which holds the twelve customers, and `orders.xml`, which holds the twenty-four orders. A third file, `orders-xxe.xml`, declares an external entity that points at a local file, which is the classic XML external entity attack. Here is the start of `customers.xml`, shortened, with `...` marking the omitted fields and customers:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<customers>
  <customer id="1001">
    <name>Alice Carter</name>
    <email>alice.carter@example.invalid</email>
    ...
    <address>
      <street>12 Maple Street</street>
      <city>Springfield</city>
      ...
    </address>
  </customer>
  ...
</customers>
```

The `id` is an attribute, and everything else is a child element. The declaration on the first line states the version and the encoding, and the rest is a single root element with a child for each customer.

**Libraries.** C# uses `System.Xml` and `System.Xml.Linq`, both part of the .NET base libraries. Python uses `lxml` 6.1.0, for `etree` and its parser settings, along with `os`. JavaScript uses `fast-xml-parser` 5.12.1 (MIT), declared in `samples\package.json`, along with `node:fs` and `node:path`. Install the JavaScript packages with `npm install` in `samples` before running the JavaScript samples.

The chapter has a reading step, four samples, two homework items, and a summary with three quizzes.

---
