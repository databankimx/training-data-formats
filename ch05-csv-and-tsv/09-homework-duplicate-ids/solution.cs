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
var records = rows.Skip(1).ToList();
var seen = new HashSet<string>();
var repeated = new List<string>();
foreach (var record in records)
{
    var id = record[0];
    if (!seen.Add(id) && !repeated.Contains(id))
    {
        repeated.Add(id);
    }
}
Console.WriteLine($"Rows: {records.Count}");
Console.WriteLine($"Unique customer ids: {seen.Count}");
var repeatedText = string.Join(", ", repeated);
Console.WriteLine($"Repeated ids: {repeatedText}");
