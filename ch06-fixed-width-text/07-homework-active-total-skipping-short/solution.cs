// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

using System.Globalization;

var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers-fixed-short-row.fixed");
var lines = File.ReadAllLines(path, System.Text.Encoding.UTF8);
const int layoutLength = 56;
var counted = 0;
var skipped = 0;
// decimal keeps each balance exact, so the total has no floating-point drift.
decimal total = 0;
foreach (var line in lines)
{
    if (line.Length < layoutLength)
    {
        skipped++;
        continue;
    }
    if (line.Substring(48, 5).Trim() == "true")
    {
        counted++;
        total += decimal.Parse(line.Substring(39, 8).Trim(), CultureInfo.InvariantCulture);
    }
}
var totalText = total.ToString("F2", CultureInfo.InvariantCulture);
Console.WriteLine($"Active customers counted: {counted}");
Console.WriteLine($"Active total: {totalText}");
Console.WriteLine($"Skipped short lines: {skipped}");
