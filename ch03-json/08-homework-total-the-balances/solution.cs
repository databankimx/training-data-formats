// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

using System.Globalization;
using System.Text.Json;

var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers.json");
using var document = JsonDocument.Parse(File.ReadAllText(path, System.Text.Encoding.UTF8));
var active = 0;
// decimal is exact for these values, so the total has no floating-point drift.
decimal total = 0;
foreach (var customer in document.RootElement.EnumerateArray())
{
    if (customer.GetProperty("active").GetBoolean())
    {
        active++;
    }
    total += customer.GetProperty("balance").GetDecimal();
}
var totalText = total.ToString("F2", CultureInfo.InvariantCulture);
Console.WriteLine($"Active customers: {active}");
Console.WriteLine($"Total balance: {totalText}");
