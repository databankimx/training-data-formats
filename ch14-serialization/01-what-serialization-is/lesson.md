# What Serialization Is

A serializer maps between two shapes: the fields of a file, and the properties of a record in a program. Each mapping makes four decisions. The first is the name: a field called `customer_id` in the file is a property called something in the program, and the two names must be matched exactly or by a rule. The second is the type: the file's `1250.75` is a number, and the program must decide whether it's a binary float, a decimal, or text, which is the decision the earlier chapters kept returning to. The third is the missing value: a field absent from the file is either a default or an error, and the mapping must say which. The fourth is the unknown field: a field the file has and the program doesn't name.

The fourth decision is the easiest to get wrong, because it's silent by default. Many libraries ignore unknown fields without a word, so a file from a newer system with a new field loads without error, and the new data is simply lost. Others refuse the file, which is safer for a strict pipeline and harder for a loose one. Neither is always right. The right choice depends on whether the file is a contract or a feed, and the sample in this chapter makes the choice visible.

A serializer is also the place where the earlier chapters' type decisions have to be made once and kept. A balance is read as a decimal, not a float, and it is written back as the same decimal. A postal code is a string everywhere, so its zeros survive. The mapping is a fixed set of decisions, and a round trip through the mapping is the test that they were made consistently.

> **Aside: a record class is a schema in code.**
> The class says which fields exist and what types they have, so it does the job of the schema from Chapter 11 for one program. A class that doesn't match the file is a schema error, and the serializer's failure is the first sign of it.

> **Common mistake.** Letting the serializer choose a type. A library that reads every number as a double will do it silently, and a balance read that way is no longer exact. Declare the type of each field in the record, and let the serializer follow the declaration.

---
