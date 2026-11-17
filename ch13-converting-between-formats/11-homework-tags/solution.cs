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
var tagColumn = Array.IndexOf(rows[0], "tags");
var total = 0;
var empty = 0;
foreach (var row in rows.Skip(1))
{
    // Empty items are dropped, so a customer with no tags has an empty list, not a list with one empty item.
    var tags = row[tagColumn].Split(';', StringSplitOptions.RemoveEmptyEntries);
    total += tags.Length;
    if (tags.Length == 0)
    {
        empty++;
    }
}
Console.WriteLine($"Tags in the list: {total}");
Console.WriteLine($"Customers with no tags: {empty}");
