# What Parquet Is

A Parquet file is laid out by column. The rows are split into groups, called row groups, and within each group every column is stored together, in its own column chunk. That's the difference from CSV and JSON Lines, which store a whole record at a time. A reader that wants one column reads only that column's chunks and skips the rest. For a wide table queried by a few columns, that saves most of the work.

The schema lives in the footer, at the end of the file. The footer holds the column names, their types, the row groups and where each chunk starts, and the statistics that let a reader skip whole row groups. A reader opens the footer first, then reads only the parts it needs. This is also why Parquet can't be read by streaming from the start in the way JSON Lines can: the schema is at the end.

The physical types are few: booleans, integers, floats, byte arrays, and fixed-length arrays. The logical types sit on top of them and say what the physical value means. A string is a byte array with a text annotation. A `decimal(10,2)` is stored as an integer with a scale of two, so `1250.75` is kept as the integer `125075` with the scale in the schema, and the arithmetic is exact. A `list` and a `struct` are nested types, stored as a set of columns that the reader reassembles into the nested value. The types are part of the file, so a reader never has to guess what `0.00` means.

Compression is per column chunk. The codec is chosen for each column, and a reader decompresses only the chunks it reads. A file produced by a data pipeline is usually compressed, which is why the sample file is far smaller than the same data as CSV.

> **Aside: why the footer matters.**
> A Parquet file that was truncated before its footer can't be read at all, because the footer holds the only map of the file. A CSV file that was truncated still gives its first rows. The format is efficient for reading and fragile for partial writes.

> **Common mistake.** Renaming a CSV file to `.parquet` to get the benefits of the format. The extension changes nothing, and every reader will refuse the file at the magic bytes. Convert the data with a library that writes Parquet.

---
