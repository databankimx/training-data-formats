// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

using System.Text.Json;

var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "orders-lines.jsonl");
var shipped = 0;
var skipped = 0;
using var reader = new StreamReader(path, System.Text.Encoding.UTF8);
string line;
while ((line = reader.ReadLine()) != null)
{
    try
    {
        using var document = JsonDocument.Parse(line);
        if (document.RootElement.GetProperty("status").GetString() == "shipped")
        {
            shipped++;
        }
    }
    catch (JsonException)
    {
        skipped++;
    }
}
Console.WriteLine($"Shipped orders: {shipped}");
Console.WriteLine($"Skipped lines: {skipped}");
