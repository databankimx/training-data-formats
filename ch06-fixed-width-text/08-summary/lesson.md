# Summary: Fixed-Width Text

This chapter covered fixed-width text, where the position of a value is its only description, and the layout is the only key to the file.

## What you learned

- A fixed-width file has no delimiter. Each field is found by its start position and width in the layout, and the layout is needed to read the file at all.
- Layout positions count from one. Code counts from zero, so a start position is reduced by one before it's used.
- Trim the padding from each cut value. Right-aligned numbers and left-aligned text are padded on opposite sides.
- A layout measured in characters and one measured in bytes disagree after the first multibyte character, so a name with an accent can move every later field.
- A short line has no value for the fields past its end. Check each line's length before cutting, and report a short line rather than padding it.
- Pad each written value to its column, and refuse a value wider than its column.
- Exact money still needs exact arithmetic. Keep the balance text, compare as numbers, and sum in decimals or whole cents.

## Quizzes

Three questions, one for each big idea in the chapter. Pick an answer, and read the explanation whichever way it goes.

```quiz
A layout places the balance at positions 40 to 47. In code, which slice takes those eight characters in Python?
○ line[40:48]
→ That's one character too far. The positions in the layout count from one, and Python's slices count from zero.
◉ line[39:47]
→ Right. The start drops by one, and the end stays where it is, so the eight characters are the same.
○ line[39:40]
→ That takes a single character. The slice needs its end as well as its start.
```

```quiz
A customer's name contains é, and the layout is measured in characters. A byte-based reader cuts the balance from the same positions. What happens?
○ The reader raises an error, so the problem is found at once.
→ A byte-based cut doesn't fail. It returns a value, and the value is wrong.
○ The balance is cut correctly, because the names are short.
→ The é moves every later byte one place to the right, so the cut lands in the wrong part of the line.
◉ The balance is cut one character early, and it returns a different number without an error.
→ Right. The result is plausible, which is why this kind of error goes unnoticed.
```

```quiz
A fixed-width file has a short line in the middle. Which handling keeps the good lines and reports the damage?
◉ Check each line's length first, skip the short one, and report its line number.
→ Right. The good lines are read, and the damage is visible to someone who can fix it.
○ Pad the short line with spaces, so every line has the same length.
→ Padding makes the missing balance look like an empty one, which is a different fact from a missing value.
○ Stop reading at the first short line.
→ That throws away every line after it, and the good records are lost with the bad one.
```

---
