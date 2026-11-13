# What JSON Is

JSON, the JavaScript Object Notation, has six kinds of value. An object is a set of name and value pairs in braces. An array is an ordered list in brackets. A string is text in double quotes. A number is a sequence of digits, which may have a minus sign, a decimal point, or an exponent. The words `true` and `false` are booleans, and `null` stands for no value. Those six are the whole language. There are no comments, no trailing commas, and no dates. A date is written as a string, and the program decides that it's a date.

The format is strict in a way that helps. A file is either valid JSON or it isn't, and a parser stops at the first error. The text is UTF-8 by convention, and the RFC that defines JSON says so. Strings use backslash escapes for quotes, backslashes, and control characters, and any other character can be written directly.

The number is where the trouble starts. JSON says a number is a sequence of digits, with optional sign, fraction, and exponent, and it says nothing about how big it may be or how many digits it keeps. `1250.75` is a number, and so is `9007199254740993`. A program still has to choose a type to hold each one. Python's integers have no size limit, so it keeps every digit. JavaScript's numbers are 64-bit floating-point values, which hold only about 15 to 17 significant digits, so `9007199254740993` silently becomes `9007199254740992`. C#'s `long` holds up to about nine quintillion, and a larger integer needs a different type.

That gap is why this chapter has a sample on large integers. The file is valid JSON, and every reader accepts it, but the value a program ends up with depends on the type it chose. A reader that doesn't say which type it used is hiding a decision.

> **Aside: null is not missing.**
> A key that holds `null` is present, with no value. A key that is absent has no value at all. A program that treats the two the same will lose a distinction the data carried, and the nulls sample shows where that matters.

> **Common mistake.** Assuming a JSON number is a decimal, so that money is safe to add up with floating point. The next homework item shows why it isn't.

---
