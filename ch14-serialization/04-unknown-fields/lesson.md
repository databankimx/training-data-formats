# Unknown Fields

A file from another system often carries fields the program was never written to use. A new loyalty field, a referrer, or an internal note arrives in a feed that the program's record doesn't name. The serializer has to do something with each one, and most libraries do the quietest thing by default: they ignore it. The data is then lost without a word, and the first sign is a report that is missing a number nobody can explain.

This sample takes the other route. It reads the fields the record declares, and it reports every field that it doesn't, with the record it came from. The two records below are typed into the code, because the point is the unknown field, and no sample file in this tutorial has one. The totals are the records read and the unknown fields found, so a reader can see that nothing was dropped.

The decision between ignoring, reporting, and refusing belongs to the program's owner. This sample reports, which keeps the data visible without stopping the run.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// Inline data, not from a sample file. Two records, typed into the code, each with a field the record type does not declare.
using System.Text.Json;
var text = "[{\"customer_id\":1001,\"name\":\"Alice Carter\",\"loyalty_points\":120},{\"customer_id\":1002,\"name\":\"Chidi Okafor\",\"referrer\":\"1001\"}]";
var known = new HashSet<string> { "customer_id", "name" };
var unknownCount = 0;
using var document = JsonDocument.Parse(text);
foreach (var record in document.RootElement.EnumerateArray())
{
    var id = record.GetProperty("customer_id").GetInt32();
    var name = record.GetProperty("name").GetString();
    Console.WriteLine($"Customer {id}: {name}");
    foreach (var property in record.EnumerateObject())
    {
        if (!known.Contains(property.Name))
        {
            unknownCount++;
            Console.WriteLine($"Unknown field: {property.Name}");
        }
    }
}
Console.WriteLine($"Customers read: {document.RootElement.GetArrayLength()}");
Console.WriteLine($"Unknown fields found: {unknownCount}");
```
```python
import json

# Inline data, not from a sample file. Two records, typed into the code, each with a field the record type does not declare.
text = '[{"customer_id":1001,"name":"Alice Carter","loyalty_points":120},{"customer_id":1002,"name":"Chidi Okafor","referrer":"1001"}]'
known = {"customer_id", "name"}
unknown_count = 0
records = json.loads(text)
for record in records:
    print(f"Customer {record['customer_id']}: {record['name']}")
    for name in record:
        if name not in known:
            unknown_count += 1
            print(f"Unknown field: {name}")
print(f"Customers read: {len(records)}")
print(f"Unknown fields found: {unknown_count}")
```
```javascript
// Inline data, not from a sample file. Two records, typed into the code, each with a field the record type does not declare.
const text = '[{"customer_id":1001,"name":"Alice Carter","loyalty_points":120},{"customer_id":1002,"name":"Chidi Okafor","referrer":"1001"}]';
const known = new Set(["customer_id", "name"]);
let unknownCount = 0;
const records = JSON.parse(text);
for (const record of records) {
  console.log(`Customer ${record.customer_id}: ${record.name}`);
  for (const name of Object.keys(record)) {
    if (!known.has(name)) {
      unknownCount++;
      console.log(`Unknown field: ${name}`);
    }
  }
}
console.log(`Customers read: ${records.length}`);
console.log(`Unknown fields found: ${unknownCount}`);
```
~~~

The output is the same in every language:

~~~text
Customer 1001: Alice Carter
Unknown field: loyalty_points
Customer 1002: Chidi Okafor
Unknown field: referrer
Customers read: 2
Unknown fields found: 2
```

The known fields are read, and each unknown field is reported in the record it came from. The count of two is the number of fields the record type doesn't declare, and it's the number to check against the source before the data is used. A feed that suddenly reports a new field tells its owner that the feed has changed, which is the information a silent serializer would have hidden.

> **Aside: ignore, report, or refuse.**
> Ignoring suits a feed whose owner has said extra fields are expected. Refusing suits a contract, where an unexpected field means the file is not the one the program was built for. Reporting sits between them, and it's the right default while a schema is still being agreed.

> **Common mistake.** Copying a record onto a class with a generic mapper and assuming that nothing is lost. The mapper drops the extra fields quietly, and the lost data is the field nobody declared. Count the fields on the way in.

---
