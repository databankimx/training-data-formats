// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package CsvHelper@33.1.0

using System.Globalization;
using CsvHelper;
using CsvHelper.Configuration;

var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "orders.csv");
var rows = new List<string[]>();
using (var csv = new CsvReader(new StreamReader(path, System.Text.Encoding.UTF8), new CsvConfiguration(CultureInfo.InvariantCulture)))
{
    while (csv.Read())
    {
        rows.Add(csv.Parser.Record);
    }
}
var customer = Array.IndexOf(rows[0], "customer_id");
var groups = rows.Skip(1).GroupBy(row => row[customer]).Select(group => group.Count()).ToList();
Console.WriteLine($"Customers with more than one order: {groups.Count(size => size > 1)}");
Console.WriteLine($"Most orders by one customer: {groups.Max()}");
