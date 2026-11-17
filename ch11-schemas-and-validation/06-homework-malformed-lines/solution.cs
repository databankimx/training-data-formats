// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

using System.Text.Json;

// Inline data, not from a sample file. The statuses an order may have.
var allowed = new HashSet<string> { "pending", "paid", "shipped", "refunded" };
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "orders-lines.jsonl");
var checkedLines = 0;
var failing = 0;
using var reader = new StreamReader(path, System.Text.Encoding.UTF8);
string line;
var number = 0;
while ((line = reader.ReadLine()) != null)
{
    number++;
    checkedLines++;
    try
    {
        using var document = JsonDocument.Parse(line);
        var status = document.RootElement.GetProperty("status").GetString() ?? "";
        if (!allowed.Contains(status))
        {
            Console.WriteLine($"Line {number}: status is not allowed");
            failing++;
        }
    }
    catch (JsonException)
    {
        Console.WriteLine($"Line {number}: not valid JSON");
        failing++;
    }
}
Console.WriteLine($"Lines checked: {checkedLines}");
Console.WriteLine($"Lines failing: {failing}");
