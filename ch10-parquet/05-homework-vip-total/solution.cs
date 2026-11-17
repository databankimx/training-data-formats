// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package Parquet.Net@5.6.1

using Parquet.Serialization;

var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers.parquet");
var customers = await ParquetSerializer.DeserializeAsync<Customer>(path);
var vip = customers.Count(customer => customer.tags.Contains("vip"));
// decimal keeps each balance exact, so the total has no floating-point drift.
decimal total = 0;
foreach (var customer in customers)
{
    total += customer.balance ?? 0;
}
var totalText = total.ToString("F2", System.Globalization.CultureInfo.InvariantCulture);
Console.WriteLine($"VIP customers: {vip}");
Console.WriteLine($"Total balance: {totalText}");

class Customer
{
    public decimal? balance { get; set; }
    public List<string> tags { get; set; } = new List<string>();
}
