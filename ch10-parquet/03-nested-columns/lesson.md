# Nested Columns

Two of the columns in `customers.parquet` are nested. The `address` column is a struct, with a street, a city, and a postal code. The `tags` column is a list of text values, which can be empty. Parquet stores each nested column as a set of flat columns, and the reader puts them back together, so a program gets the nested value back as it was written.

The sample below reads the first customer's city and tags, and counts the customers whose tags list is empty. An empty list is a value, not a missing one, so those customers still have a row and a list, with nothing in it. The count checks that the reader keeps the empty lists rather than dropping them.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package Parquet.Net@5.6.1

// The sample file is read from the folder named by TRAINING_DATA. The struct and the list come back as nested values.
using Parquet.Serialization;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers.parquet");
var customers = await ParquetSerializer.DeserializeAsync<Customer>(path);
var first = customers[0];
var tags = string.Join(", ", first.tags);
var noTags = customers.Count(customer => customer.tags.Count == 0);
Console.WriteLine($"City of 1001: {first.address.city}");
Console.WriteLine($"Tags of 1001: {tags}");
Console.WriteLine($"Customers with no tags: {noTags}");

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

# The sample file is read from the folder named by TRAINING_DATA. The struct arrives as a dict, and the list as a list.
path = os.path.join(os.environ["TRAINING_DATA"], "customers.parquet")
rows = pq.read_table(path).to_pylist()
first = rows[0]
no_tags = sum(1 for row in rows if not row["tags"])
print(f"City of 1001: {first['address']['city']}")
print(f"Tags of 1001: {', '.join(first['tags'])}")
print(f"Customers with no tags: {no_tags}")
```
```javascript
import path from "node:path";
import { asyncBufferFromFile, parquetReadObjects } from "hyparquet";

// The sample file is read from the folder named by TRAINING_DATA. The struct arrives as an object, and the list as an array.
const rows = await parquetReadObjects({ file: await asyncBufferFromFile(path.join(process.env.TRAINING_DATA, "customers.parquet")) });
const first = rows[0];
const noTags = rows.filter((row) => row.tags.length === 0).length;
console.log(`City of 1001: ${first.address.city}`);
console.log(`Tags of 1001: ${first.tags.join(", ")}`);
console.log(`Customers with no tags: ${noTags}`);
```
~~~

The output is the same in every language:

~~~text
City of 1001: Springfield
Tags of 1001: vip, newsletter
Customers with no tags: 2
~~~

The two customers with no tags are the second and the seventh, Okafor and Ribeiro. Their tag lists are empty, not null, and the sample counts them as rows with no tags. A reader that loses the empty list would see a shorter count, or fail on the missing value.

The struct is read as a nested value, so the city is reached through the address. In C# and Python the nested value is a class or dictionary, and in JavaScript it's an object. The structure matches the file, and no column names have been flattened.

> **Aside: flattening a nested column loses its shape.**
> A flat table can't say which postal code belongs to which address when a row has several. Parquet keeps the struct and the list together, and a flattened copy gives up that structure, as the XML and YAML chapters showed for their own nested data.

> **Common mistake.** Testing for empty tags with `tags is None`. An empty list is not a null, so that test is false for every customer. Test the length, as the sample does.

---
