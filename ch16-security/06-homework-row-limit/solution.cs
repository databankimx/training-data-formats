// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

using System.Text;

var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers.csv");
const int limit = 10;
var accepted = 0;
var refused = 0;
var first = true;
foreach (var line in File.ReadLines(path, Encoding.UTF8))
{
    if (first)
    {
        // The header is not a data row, so it is skipped before the count begins.
        first = false;
        continue;
    }
    if (accepted < limit)
    {
        accepted++;
    }
    else
    {
        refused++;
    }
}
Console.WriteLine($"Rows accepted: {accepted}");
Console.WriteLine($"Rows refused: {refused}");
