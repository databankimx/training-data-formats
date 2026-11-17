# Summary: YAML

This chapter covered YAML: indentation as structure, plain values whose types are chosen by the reader, and the rule that a file from outside your system is loaded with the safe loader.

## What you learned

- YAML has mappings, sequences, and scalars. Indentation is the structure, and it must be spaces.
- A quoted value is a string in every reader. A plain value's type depends on the reader.
- The YAML version matters. YAML 1.1 reads `NO` and `on` as booleans, and YAML 1.2 reads them as text.
- A round trip is the right test for a writer. The layout differs between libraries, and the data should not.
- A file written for one YAML version can be read wrongly by another, with no error.
- A file from outside your system is loaded with the safe loader. A loader that builds named types can run behaviour the file asks for.
- A tab used for indentation is refused. Catch the parser's own error, and let other errors stop the program.
- Compare values as text when they identify something, such as a country code, and quote them in the file.

## Quizzes

Three questions, one for each big idea in the chapter. Pick an answer, and read the explanation whichever way it goes.

```quiz
A YAML file contains country_code: NO without quotes. A reader follows YAML 1.1. What does the program receive?
○ The text NO, because the reader keeps every plain value as text.
→ That's YAML 1.2 behaviour. Under YAML 1.1, the bare word is read as a boolean.
◉ The boolean false, because YAML 1.1 reads NO as a boolean.
→ Right. The value changes type without any error, which is why a country code should be quoted.
○ An error, because NO is not a valid value.
→ The reader accepts the value and changes its type. Nothing is reported.
```

```quiz
A customer file was written by one library and read by another. The layouts are different, but the values match. What does that show?
○ That the writer has a bug, because the text differs.
→ Different layouts are normal. Two libraries can write the same data with different text.
○ That the reader must be the same library as the writer.
→ Any reader that follows the same YAML version can read the data.
◉ That the test of a writer is the round trip, because the data is what matters, not the layout.
→ Right. A round trip compares the meaning of the data, which is what a receiving program depends on.
```

```quiz
A YAML file loaded from another company's system uses a tag that names a type. Which loader is right?
◉ The safe loader, which builds only plain values such as strings, numbers, lists, and maps.
→ Right. A loader that builds named types can run behaviour that the file requests.
○ The full loader, so that the named type is created as the file asks.
→ That would let the file choose what the program runs. Use the safe loader for any file from outside.
○ Whichever loader is first in the documentation, because they all give the same result.
→ They do not. Some loaders build arbitrary types, and the choice matters for security.
```

---
