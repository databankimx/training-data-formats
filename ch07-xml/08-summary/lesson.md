# Summary: XML

This chapter covered XML as a tree: its elements, attributes, namespaces, and the external entities that make a parser dangerous to point at untrusted input.

## What you learned

- An XML document is a tree with one root. Elements hold text or children, and attributes hold metadata on the element.
- A document is well formed when it follows the syntax, and valid when it also conforms to a schema. The safety question is about the parser, not the schema.
- A namespace is identified by its URI, not its prefix. Compare by namespace and local name.
- An entity declared in a DOCTYPE can point at a local file. A parser that resolves it will read that file.
- Each language's safe setting is different. C# refuses DTDs, Python refuses to resolve external entities, and JavaScript refuses external entities by default. Set one explicitly, and test it with a reference to a local file.
- `no_network` does not stop a local file reference. Only the entity setting does.
- The library writes the escapes when it writes the tree. Hand-written XML with an unescaped ampersand is invalid.
- Compare identifiers by their attribute, not by a child element of the same name.

## Quizzes

Three questions, one for each big idea in the chapter. Pick an answer, and read the explanation whichever way it goes.

```quiz
Two XML documents use the same namespace URI, one with the prefix ns and one with the prefix o. What is the correct way for a program to match their order elements?
○ Match the text ns:order, because that is the name in the first document.
→ The second document doesn't use that text, so the match fails on a document that is correct.
◉ Match the namespace URI and the local name order, which are the same in both documents.
→ Right. The prefix is a shorthand chosen by each author, so the URI and local name are what a program compares.
○ Match the element by position in the file, because the order is the same.
→ Position depends on the file, and two files can list the same orders in a different order.
```

```quiz
A parser is set with resolve_entities=False and no_network=True, and it reads a document whose entity points at a local file. What happens?
○ The network setting blocks the read, so the file is never opened.
→ A local file reference is not a network request, so the network setting doesn't stop it.
○ The parser raises an error, so nothing is read.
→ The parser may accept the document. The setting that matters is the one that refuses entity resolution.
◉ The file contents are not placed in the note, because resolve_entities=False leaves the reference unresolved.
→ Right. The entity setting is the one that stops the file being read, and it's the only setting that does.
```

```quiz
A program builds an XML note by joining the text Tom & Jerry between tags. What goes wrong?
◉ The ampersand is not escaped, so the document is invalid and a parser stops at it.
→ Right. A library writes the escape for you, and joining strings by hand leaves the ampersand as it is.
○ The note is written correctly, because the ampersand is ordinary text.
→ In XML an ampersand begins an entity reference, so it must be written as &amp;.
○ The note is written, but a reader will treat the ampersand as a comment.
→ Comments use a different syntax, and an ampersand is not a comment marker.
```

---
