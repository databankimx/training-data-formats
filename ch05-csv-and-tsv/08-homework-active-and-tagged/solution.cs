// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package CsvHelper@33.1.0

using System.Globalization;
using CsvHelper;
using CsvHelper.Configuration;

var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers.csv");
var rows = new List<string[]>();
using (var csv = new CsvReader(new StreamReader(path, System.Text.Encoding.UTF8), new CsvConfiguration(CultureInfo.InvariantCulture)))
{
    while (csv.Read())
    {
        rows.Add(csv.Parser.Record);
    }
}
var active = 0;
var tagged = 0;
foreach (var row in rows.Skip(1))
{
    // Column 5 is active, and column 10 is tags.
    if (row[5] == "true")
    {
        active++;
    }
    if (row[10].Length > 0)
    {
        tagged++;
    }
}
Console.WriteLine($"Active customers: {active}");
Console.WriteLine($"Tagged customers: {tagged}");
