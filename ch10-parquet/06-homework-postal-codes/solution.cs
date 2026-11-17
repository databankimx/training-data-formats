// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package Parquet.Net@5.6.1

using Parquet.Serialization;

var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers.parquet");
var customers = await ParquetSerializer.DeserializeAsync<Customer>(path);
// The postal code is text, so its leading zeros are kept, and the first character is tested.
var zeroStart = customers.Count(customer => customer.address.postal_code.StartsWith('0'));
Console.WriteLine($"Postal codes starting with 0: {zeroStart}");

class Customer
{
    public Address address { get; set; } = new Address();
}

class Address
{
    public string postal_code { get; set; } = "";
}
