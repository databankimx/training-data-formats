# Reading Parquet

Reading a Parquet file gives you rows, with each value in the type the footer declares. The sample below reads `customers.parquet`, counts the customers, and prints the first one. The balance comes back as a decimal, so it keeps the two places the file stores, and the identifier comes back as an integer.

The C# version maps the file onto a class whose properties match the column names. The file marks its columns as optional, so the C# properties for numbers, booleans, and dates are nullable, with a question mark. The reader checks that the class and the file agree on this, and a required property against an optional column stops the program. Python and JavaScript read the rows as they are. The output is the same in each language.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package Parquet.Net@5.6.1

// The sample file is read from the folder named by TRAINING_DATA. Each row is read into a class with the stored types.
using Parquet.Serialization;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers.parquet");
var customers = await ParquetSerializer.DeserializeAsync<Customer>(path);
var first = customers[0];
Console.WriteLine($"Records: {customers.Count}");
Console.WriteLine($"First customer: {first.customer_id} {first.name} {first.balance}");

class Customer
{
    public long? customer_id { get; set; }
    public string name { get; set; } = "";
    public string email { get; set; } = "";
    public DateTime? signup_date { get; set; }
    public decimal? balance { get; set; }
    public bool? active { get; set; }
    public string country_code { get; set; } = "";
    public Address address { get; set; } = new Address();
    public List<string> tags { get; set; } = new List<string>();
}

class Address
{
    public string street { get; set; } = "";
    public string city { get; set; } = "";
    public string postal_code { get; set; } = "";
}
```
```python
import os

import pyarrow.parquet as pq

# The sample file is read from the folder named by TRAINING_DATA. Each row is read with the types the footer declares.
path = os.path.join(os.environ["TRAINING_DATA"], "customers.parquet")
rows = pq.read_table(path).to_pylist()
first = rows[0]
print(f"Records: {len(rows)}")
print(f"First customer: {first['customer_id']} {first['name']} {first['balance']}")
```
```javascript
import path from "node:path";
import { asyncBufferFromFile, parquetReadObjects } from "hyparquet";

// The sample file is read from the folder named by TRAINING_DATA. Each row is read with the types the footer declares.
const rows = await parquetReadObjects({ file: await asyncBufferFromFile(path.join(process.env.TRAINING_DATA, "customers.parquet")) });
const first = rows[0];
console.log(`Records: ${rows.length}`);
console.log(`First customer: ${first.customer_id} ${first.name} ${first.balance}`);
```
~~~

The output is the same in every language:

~~~text
Records: 12
First customer: 1001 Alice Carter 1250.75
~~~

The balance prints as `1250.75`, and the stored decimal would print `1250.75` in every language. The file stores the balance as a scaled integer, so no conversion has rounded it. A CSV reader would have seen the text `1250.75`, and an Excel reader would have seen the number, but the Parquet reader sees the type that was written.

The C# class is a mapping, so its property names must match the column names exactly, and a column the class doesn't declare is left out. The Python and JavaScript readers return every column under its own name.

> **Aside: the reader trusts the footer.**
> A reader that gets a file with a wrong footer, or a column the schema doesn't match, returns values according to that footer. A check on the row count and on the first row, as in this sample, catches the most common mistakes.

> **Aside: the class must match the file's nullability.**
> A Parquet column can be required or optional, and the file records which. A C# property of type `long` or `decimal` is required, so reading an optional column into it stops with a message about definition levels. The fix is the nullable form, `long?` or `decimal?`, which matches an optional column. Reference types such as `string` already allow null, so they need no change. Check the file's columns in the viewer before you write the class.

> **Common mistake.** Reading the balance as a float because it looks like a number. A float is close to `1250.75` but not equal to it, and a total of many floats drifts. Keep the decimal type all the way through.

---
