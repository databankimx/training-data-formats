// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package CsvHelper@33.1.0

using System.Globalization;
using CsvHelper;
using CsvHelper.Configuration;

var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers-duplicates.csv");
var rows = new List<string[]>();
using (var csv = new CsvReader(new StreamReader(path, System.Text.Encoding.UTF8), new CsvConfiguration(CultureInfo.InvariantCulture)))
{
    while (csv.Read())
    {
        rows.Add(csv.Parser.Record);
    }
}
var body = rows.Skip(1).ToList();
var seen = new HashSet<string>();
var failing = 0;
for (var index = 0; index < body.Count; index++)
{
    var id = body[index][0];
    // A row fails when its identifier has already appeared on an earlier row.
    if (!seen.Add(id))
    {
        Console.WriteLine($"Line {index + 2}: customer_id {id} is a duplicate");
        failing++;
    }
}
Console.WriteLine($"Rows checked: {body.Count}");
Console.WriteLine($"Rows failing: {failing}");
