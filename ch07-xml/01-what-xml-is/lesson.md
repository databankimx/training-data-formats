# What XML Is

An XML document is a tree. It has one root element, and every other element sits inside it. An element has a name, written in angle brackets, and it contains text, child elements, or both. An element can also have attributes, which are name and value pairs inside the opening tag. In `customers.xml`, `id` is an attribute of `customer`, and `name` is a child element. Attributes hold metadata about an element, and child elements hold its content. The distinction is a convention, not a rule the parser enforces, and different schemas make different choices.

A document is well formed when it follows the syntax: every opening tag has a closing tag, the elements nest correctly, and there's exactly one root. A parser rejects a document that breaks any of these rules. A document is valid when it also conforms to a schema, such as a DTD or an XSD, which says which elements may appear and in what order. This chapter is about well-formed documents, and the entity problem belongs to the parser, not the schema.

Namespaces solve a naming clash. Two documents may both have an element called `order`, and when they're combined, the names collide. A namespace gives the name a URI, written in a declaration such as `xmlns:ns="urn:example:orders"`. The element is then `ns:order`, and a parser compares the URI, not the prefix. The prefix is only a short label, and two documents can use different prefixes for the same namespace. A program that matches on the prefix will fail the day someone renames it.

Entities are where XML becomes a risk. A document can declare its own entity in a DOCTYPE, which is a named text replacement that the parser expands wherever the name appears. An entity can also point at an external resource, using a `SYSTEM` identifier that names a file or a URL. A parser that resolves external entities will read that file and place its content into the document. `orders-xxe.xml` declares exactly that, pointing at a file on the local disk, and the note field of an order would carry the file's contents to whoever receives the parsed data.

The defence is a parser setting. Refusing DTDs entirely is the safest, and refusing external entities while allowing internal ones is the next choice. The default setting differs by library, so the chapter's samples set it explicitly rather than trusting the default.

> **Aside: XML is not JSON with angle brackets.**
> A JSON object has keys and values. An XML element can have both attributes and children, and both can carry data, which is why the same information can be written two ways. A converter from XML to JSON has to make a choice about attributes, and the choice has to be written down.

> **Common mistake.** Trusting a parser's default settings for untrusted input. A library may resolve external entities by default, and the default is part of the attack surface. Set the safe option explicitly, and test it with a file like `orders-xxe.xml`.

---
