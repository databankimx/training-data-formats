# Summary: JSON

This chapter covered JSON from reading to writing, and the places where a parser decides something for you.

## What you learned

- JSON has six kinds of value. A number has no integer or decimal type, so each program chooses one.
- Reading parses the whole array into the language's own objects. Writing turns values back into text, and the writer keeps the order you gave.
- A flattened key such as `address.city` can hold a value but not the object it came from. Choose a separator that can't occur in a key.
- A null is present with no value. A missing key has no value at all. An empty string is a third case. Tell them apart with a test that asks about the key itself.
- A JavaScript number holds only about 15 to 17 significant digits, so a larger identifier is silently changed. Python keeps every digit, and C#'s `decimal` is exact for whole numbers up to 28 digits.
- Money needs exact arithmetic. Use a decimal type, or whole cents, rather than binary floats.
- A truncated file fails to parse, and the start of the file still shows that it is JSON. Catch the parse error only, and report the file as incomplete.

## Quizzes

Three questions, one for each big idea in the chapter. Pick an answer, and read the explanation whichever way it goes.

```quiz
A JSON file holds the number 9007199254740993. A JavaScript program reads it with JSON.parse and prints the value. What does it print?
◉ 9007199254740992, because a 64-bit float can't hold that digit.
→ Right. The value is one past the limit, so it rounds to the nearest float. JavaScript raises no error.
○ 9007199254740993, because JSON.parse keeps every digit.
→ JSON.parse stores numbers as 64-bit floats, which lose the last digit at this size.
○ An error, because the number is too large.
→ JavaScript doesn't raise an error here. It silently stores the nearest value it can.
```

```quiz
A customer record has "email": null, and another has no email key. What is the right test to tell them apart?
○ if (record.email), because a null and a missing key are both false.
→ That test is false for both, so it can't tell them apart. It also fails for an empty string.
○ if (record.email === undefined), because a null is undefined in JavaScript.
→ A null is not undefined. The missing key is the one that gives undefined.
◉ Ask whether the key is present, with the in operator or TryGetProperty, then check whether its value is null.
→ Right. Presence and value are separate questions, so the test asks each one in turn.
```

```quiz
A file starts with [ but ends halfway through a customer record. What does a careful program report?
○ That the file is binary, because part of it is missing.
→ The start of the file is text, and the damage is in the middle, not in the type.
◉ That the file doesn't parse, and that it starts like JSON, so it is probably incomplete.
→ Right. The parse failure and the start of the file are two separate facts, and both go in the report.
○ That the file is valid, because the start is correct.
→ A parser reads the whole file, so the start being correct doesn't make the file valid.
```

---
