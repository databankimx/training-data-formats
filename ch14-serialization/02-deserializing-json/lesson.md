# Deserializing JSON

This sample reads `customers.json` and maps each object onto a record type that the program declares. The record has a property for every field, and the address is its own type, so the nested object maps onto a nested record. The record is the schema for the program, and the mapping is checked against it when the file is read.

Each language declares the record in its own way. C# uses a class, Python uses a dataclass, and JavaScript uses a class with a constructor. The balance is the field to watch. C# and Python declare it as a decimal and read the file's number as one, so the value is exact. JavaScript has no decimal type, so its balance is a number, a binary float, the same limit the earlier chapters described. The sample prints the balance so the difference is visible.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// The sample file is read from the folder named by TRAINING_DATA. Each object is mapped onto a Customer, with the balance as a decimal.
using System.Text.Json;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers.json");
var customers = JsonSerializer.Deserialize<List<Customer>>(File.ReadAllText(path, System.Text.Encoding.UTF8));
var first = customers[0];
Console.WriteLine($"Customers: {customers.Count}");
Console.WriteLine($"First customer: {first.customer_id} {first.name} {first.balance}");

class Customer
{
    public int customer_id { get; set; }
    public string name { get; set; } = "";
    public string email { get; set; } = "";
    public string signup_date { get; set; } = "";
    public decimal balance { get; set; }
    public bool active { get; set; }
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
import json
import os
from dataclasses import dataclass, field
from decimal import Decimal

# The sample file is read from the folder named by TRAINING_DATA. Each object is mapped onto a Customer, with the balance as a Decimal.
@dataclass
class Address:
    street: str
    city: str
    postal_code: str


@dataclass
class Customer:
    customer_id: int
    name: str
    email: str
    signup_date: str
    balance: Decimal
    active: bool
    country_code: str
    address: Address
    tags: list = field(default_factory=list)


path = os.path.join(os.environ["TRAINING_DATA"], "customers.json")
with open(path, encoding="utf-8") as handle:
    records = json.load(handle, parse_float=Decimal)
customers = [Customer(**{**record, "address": Address(**record["address"])}) for record in records]
first = customers[0]
print(f"Customers: {len(customers)}")
print(f"First customer: {first.customer_id} {first.name} {first.balance}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";

// The sample file is read from the folder named by TRAINING_DATA. Each object is mapped onto a Customer, with the balance as a number.
class Address {
  constructor({ street, city, postal_code }) {
    this.street = street;
    this.city = city;
    this.postal_code = postal_code;
  }
}

class Customer {
  constructor(record) {
    this.customer_id = record.customer_id;
    this.name = record.name;
    this.email = record.email;
    this.signup_date = record.signup_date;
    this.balance = record.balance;
    this.active = record.active;
    this.country_code = record.country_code;
    this.address = new Address(record.address);
    this.tags = record.tags;
  }
}

const customers = JSON.parse(readFileSync(path.join(process.env.TRAINING_DATA, "customers.json"), "utf8")).map((record) => new Customer(record));
const first = customers[0];
console.log(`Customers: ${customers.length}`);
console.log(`First customer: ${first.customer_id} ${first.name} ${first.balance}`);
```
~~~

The output is the same in every language:

~~~text
Customers: 12
First customer: 1001 Alice Carter 1250.75
~~~

The three versions map the same fields by name, and each nested object becomes its own record. The output is identical here because `1250.75` happens to be exact as a binary float, since its fraction is three quarters. A balance such as `0.10` is not exact in binary, and the homework that follows relies on that.

> **Aside: the constructor is where the mapping is checked.**
> A record that is built from a file without checking its fields accepts whatever the file held. The JavaScript constructor reads named fields, so a misnamed field becomes `undefined`, and the error appears later, far from the cause. The Python record fails when a field is missing, and the C# record fills a missing property with its default. Both behaviours are choices, and the chapter's later samples say which one a file needs.

> **Common mistake.** Declaring the balance as a float or a double in the record because the file's number looks like one. The record then holds a binary float, and a total over many records drifts. Declare the type you need.

---
