# Summary: Serialization and Deserialization

This chapter covered the mapping between a file's fields and a program's records, and the decisions that mapping makes.

## What you learned

- A serializer makes four decisions: the name of each field, its type, what to do with a missing value, and what to do with an unknown field.
- A record type declares the schema for one program, and a mismatch between the record and the file is a schema error.
- A balance is declared as a decimal, so it stays exact. A binary float holds some decimals only approximately, and a total over many records drifts.
- JSON has no decimal type, so a decimal is written as a number in C#, as text in Python, and as a number in JavaScript. Each choice reads back to the same value.
- A round trip through a mapping tests that the decisions were made consistently. Compare values, not the text of the file.
- An unknown field is reported, not silently dropped, unless the program's owner has decided to ignore it. Count the fields on the way in.

## Quizzes

Three questions, one for each big idea in the chapter. Pick an answer, and read the explanation whichever way it goes.

```quiz
A record type declares balance as a double, and a file holds 0.10 and 0.20 in two records. What is the risk?
○ There is no risk, because a double holds every decimal exactly.
→ A double holds many decimals only approximately, and 0.10 is one of them.
◉ A total of the balances can drift from the exact sum, because the stored values are approximate.
→ Right. The error is small per value and grows with each addition, which is why balances are declared as decimals.
○ The file fails to load, because the double cannot read the number.
→ The double reads the number without error. The risk is in the arithmetic, and it is silent.
```

```quiz
A file from another system has a field the record type does not declare. A library drops it without a word. What is the best response?
○ Accept the loss, because the record type is the authority on what the data is.
→ The field may matter to the other system, and a silent drop hides the change.
○ Refuse the whole file, because any unknown field means the file is wrong.
→ That suits a strict contract, but a feed that adds a field would stop entirely. Reporting is the usual default.
◉ Report the unknown field with its record, so the change is visible and the run can continue.
→ Right. The count and the report let the owner decide whether to ignore, refuse, or extend the record type.
```

```quiz
A round trip through a mapping gives the same balances, but the JSON text of the file differs from the original. What does that show?
◉ That the comparison should check values, because the writers may format the same value differently.
→ Right. A comparison of text would fail for a harmless difference in the writer.
○ That the round trip has failed, because the text must be identical.
→ The text of a number can differ between writers without any change in its value.
○ That the mapping has lost a field, because the text is shorter.
→ Length is not a test of content. Check each field's value.
```

---
