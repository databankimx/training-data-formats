# What Conversion Is

Every fact in the dataset falls into one of three groups after a conversion. A fact is kept when it reads back exactly as it was written. A fact is changed in form when its meaning survives but its representation differs, such as a list written as a semicolon-separated string. A fact is lost when the target format cannot hold it, or when the converter drops it. A conversion is safe when every fact is kept or changed in form, and any loss is known and recorded.

The customer data has seven kinds of fact that matter here: text, whole numbers, exact decimals, booleans, dates, lists, and nested objects. The table below shows what each format does with them. It describes the usual behaviour, and each sample in this chapter checks it for the dataset.

| Format | Lists | Nested objects | Exact decimals | Leading zeros | Booleans | Dates |
|---|---|---|---|---|---|---|
| CSV | changed (joined text) | changed (flattened columns) | kept as text | kept as text | kept as text | kept as text |
| TSV | changed (joined text) | changed (flattened columns) | kept as text | kept as text | kept as text | kept as text |
| JSON | kept | kept | kept only as text | kept as text | kept | kept as text |
| JSON Lines | kept | kept | kept only as text | kept as text | kept | kept as text |
| XML | changed (repeated elements) | kept | kept as text | kept as text | kept as text | kept as text |
| YAML | kept | kept | kept only as text | kept if quoted | kept | kept if quoted |
| Fixed-width | changed (joined text) | changed (flattened columns) | kept as text | kept as text | kept as text | kept as text |
| Excel | changed (joined text) | changed (flattened columns) | kept as a number | kept only as text | kept | kept as text |
| Parquet | kept | kept | kept exactly | kept | kept | kept as a date type |

A few entries need explaining. JSON has no decimal type, so a balance written as a JSON number is read back as a binary float unless the balance is kept as text. Excel stores a balance as a number, which is exact to the precision Excel keeps, but it stores a postal code as a number if the writer does, and then the leading zero is gone. Parquet keeps a decimal as a scaled integer, so it is exact, and it keeps the type of each column when the schema is written. The dataset's postal codes are text, so every format keeps them as long as the converter writes them as text.

The check for a conversion is the comparison at the end of the loop. The data goes through every format and comes back to CSV, and the result is compared with the original. A matching result proves that the facts survived every write and every read along the way. It does not prove that any single format is the right one for the job, and a loss that is undone later in the loop, as the balance is, can hide where it happened, so the lesson on each link says what that link does to each fact.

> **Aside: a conversion is a decision about types.**
> When a converter writes a value, it chooses a type for it. When it reads the value back, it chooses a type again. Both choices must agree, or the value changes even when the bytes are right.

> **Common mistake.** Checking a conversion by counting rows. The row count matches, and a postal code or a balance has changed. Compare the values, field by field, after the round trip.

---
