# Writing Parquet

Writing Parquet means choosing a type for each column and letting the library lay out the row groups, chunks, and footer. The types are the important part. A balance written as a decimal is stored as a decimal, and a list of tags is stored as a list. The sample below writes two customers from the code, reads the file back, and checks the first balance.

The file is written to the run folder, so the shared sample data is not changed. The C# and Python versions write a decimal balance. The JavaScript version writes a floating-point number, because its writer takes a column type as a name, and the lesson returns to that choice.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package Parquet.Net@5.6.1

// Inline data, not from a sample file. Two customers, typed into the code, with a decimal balance and a list of tags.
using Parquet.Serialization;
var customers = new List<Customer>
{
    new Customer { customer_id = 1001, name = "Alice Carter", balance = 1250.75m, active = true, tags = new List<string> { "vip", "newsletter" } },
    new Customer { customer_id = 1002, name = "Chidi Okafor", balance = 0.00m, active = false, tags = new List<string>() },
};
await ParquetSerializer.SerializeAsync(customers, "written-customers.parquet");

// Read the file back and check the first balance.
var reopened = await ParquetSerializer.DeserializeAsync<Customer>("written-customers.parquet");
Console.WriteLine($"Rows read back: {reopened.Count}");
Console.WriteLine($"Balance in row 1: {reopened[0].balance}");

class Customer
{
    public long? customer_id { get; set; }
    public string name { get; set; } = "";
    public decimal? balance { get; set; }
    public bool? active { get; set; }
    public List<string> tags { get; set; } = new List<string>();
}
```
```python
import pyarrow as pa
import pyarrow.parquet as pq
from decimal import Decimal

# Inline data, not from a sample file. Two customers, typed into the code, with a decimal balance and a list of tags.
table = pa.table(
    {
        "customer_id": pa.array([1001, 1002], type=pa.int64()),
        "name": ["Alice Carter", "Chidi Okafor"],
        "balance": pa.array([Decimal("1250.75"), Decimal("0.00")], type=pa.decimal128(10, 2)),
        "active": [True, False],
        "tags": [["vip", "newsletter"], []],
    }
)
pq.write_table(table, "written-customers.parquet")

# Read the file back and check the first balance.
rows = pq.read_table("written-customers.parquet").to_pylist()
print(f"Rows read back: {len(rows)}")
print(f"Balance in row 1: {rows[0]['balance']}")
```
```javascript
import { asyncBufferFromFile, parquetReadObjects } from "hyparquet";
import { parquetWriteFile } from "hyparquet-writer";

// Inline data, not from a sample file. Two customers, typed into the code, with a balance and a list of tags.
await parquetWriteFile({
  filename: "written-customers.parquet",
  columnData: [
    { name: "customer_id", data: [1001n, 1002n], type: "INT64" },
    { name: "name", data: ["Alice Carter", "Chidi Okafor"], type: "STRING" },
    { name: "balance", data: [1250.75, 0], type: "DOUBLE" },
    { name: "active", data: [true, false], type: "BOOLEAN" },
  ],
});

// Read the file back and check the first balance.
const rows = await parquetReadObjects({ file: await asyncBufferFromFile("written-customers.parquet") });
console.log(`Rows read back: ${rows.length}`);
console.log(`Balance in row 1: ${rows[0].balance}`);
```
~~~

The output is the same in every language:

~~~text
Rows read back: 2
Balance in row 1: 1250.75
~~~

Both checks pass. The file holds two rows, and the first balance is the same number that went in. The balance is stored as a decimal in the C# and Python files, and as a double in the JavaScript file, so the printed value is the same here but the stored type is not.

The JavaScript writer is given a type name for each column, and `DOUBLE` is a floating-point value. A balance stored as a double is exact only for values that a binary float can hold, and a total of many doubles drifts. The homework takes the exact route, so the JavaScript sample is a warning rather than a model: when balances must be exact, write them as a decimal, or as whole cents in an integer column.

> **Aside: the writer records the type you chose.**
> Parquet keeps the type given to the writer. A balance written as text is read back as text, and no reader can recover the decimal the data was meant to be.

> **Common mistake.** Writing a balance as a double because it's the default for a float in the language. The value looks right on screen, and the arithmetic later on is slightly wrong.

---
