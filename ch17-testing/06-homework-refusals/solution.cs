// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

using System.Text.Json;

// Inline data, not from a sample file. Four inputs, typed into the code, sent to a JSON reader.
var inputs = new[] { "[{\"a\":1}]", "[{\"a\":", "", "{\"a\":1}" };
var refused = 0;
var accepted = 0;
foreach (var input in inputs)
{
    try
    {
        JsonDocument.Parse(input);
        accepted++;
    }
    catch (JsonException)
    {
        refused++;
    }
}
Console.WriteLine($"Refused: {refused}");
Console.WriteLine($"Accepted: {accepted}");
