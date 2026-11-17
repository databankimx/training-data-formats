# What Fixed-Width Text Is

A fixed-width file has no separators. Each field occupies a range of positions, and the same range holds the same field in every line. These often come from older mainframe application output or databases that implement fixed character width columns. The file doesn't say where the fields are, so a separate layout does, and this chapter's layout is `customers.fixed.layout.txt`. It gives each column a start position, a width, and an alignment.

| Column | Start | Width | Alignment |
|---|---|---|---|
| customer_id | 1 | 6 | right |
| name | 8 | 20 | left |
| signup_date | 29 | 10 | left |
| balance | 40 | 8 | right |
| active | 49 | 5 | left |
| country_code | 55 | 2 | left |

Positions in the layout count from one, and the ranges are inclusive. The name occupies positions 8 to 27, so the name's first letter is at position 8 and its last possible letter is at position 27. A reader in a language that counts from zero subtracts one from each start. The sample code does that, and the lesson returns to the difference whenever it matters.

Alignment decides where the spaces go. A number is right-aligned, so its leading spaces pad the left of the field and its digits end at the right edge. A text value is left-aligned, so its trailing spaces pad the right. A reader that trims both sides gets the same value either way, which is why trimming is the usual first step.

The layout is part of the data. Without it, a line of digits and spaces is just text. Keep the layout beside the file, version it with the file, and treat a change to the layout as a change to the format, because an old reader given a new layout will misread every line.

Two things break a fixed-width reader. The first is a line that's too short. Reading past its end is an error in some languages and a silent shortened value in others, and the short-row sample shows both. The second is a character that takes more than one byte. A layout measured in bytes puts every later field one position off, and the next sample shows how.

> **Aside: why layouts were used.**
> A fixed layout needs no delimiter, no quoting, and no escaping. A value can contain any character without changing the structure, and the file stays small. The cost is that every field has a width fixed in advance, and a value wider than its column has nowhere to go.

> **Common mistake.** Assuming the layout's width is the width of the value. A balance of `4410.00` fits its 8-column field with a space to spare. A balance of `-14410.00` has nine characters, and it has nowhere to go in an 8-column field, so the reader has to refuse it rather than let it spill into the next column.

---
