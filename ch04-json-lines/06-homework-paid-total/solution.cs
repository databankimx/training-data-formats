// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

using System.Globalization;
using System.Text.Json;

var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "orders-lines.jsonl");
var paidCount = 0;
// decimal keeps each amount exact, so the sum has no floating-point drift.
decimal total = 0;
using var reader = new StreamReader(path, System.Text.Encoding.UTF8);
string line;
while ((line = reader.ReadLine()) != null)
{
    try
    {
        using var document = JsonDocument.Parse(line);
        var order = document.RootElement;
        if (order.GetProperty("status").GetString() == "paid")
        {
            paidCount++;
            total += decimal.Parse(order.GetProperty("amount").GetString(), CultureInfo.InvariantCulture);
        }
    }
    catch (JsonException)
    {
        // The damaged line is skipped, and reading goes on.
    }
}
var totalText = total.ToString("F2", CultureInfo.InvariantCulture);
Console.WriteLine($"Paid orders: {paidCount}");
Console.WriteLine($"Paid total: {totalText}");
