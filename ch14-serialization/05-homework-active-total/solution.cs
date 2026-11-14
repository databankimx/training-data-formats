// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

using System.Globalization;
using System.Text.Json;

var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers.json");
var customers = JsonSerializer.Deserialize<List<Customer>>(File.ReadAllText(path, System.Text.Encoding.UTF8));
var active = 0;
// decimal keeps each balance exact, so the total has no floating-point drift.
decimal total = 0;
foreach (var customer in customers)
{
    if (customer.active)
    {
        active++;
        total += customer.balance;
    }
}
var totalText = total.ToString("F2", CultureInfo.InvariantCulture);
Console.WriteLine($"Active customers: {active}");
Console.WriteLine($"Active total: {totalText}");

class Customer
{
    public int customer_id { get; set; }
    public bool active { get; set; }
    public decimal balance { get; set; }
}
