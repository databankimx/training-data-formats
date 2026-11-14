// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package CsvHelper@33.1.0

using System.Globalization;
using System.Text.RegularExpressions;
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
var column = Array.IndexOf(rows[0], "address_postal_code");
var changed = 0;
foreach (var row in rows.Skip(1))
{
    var code = row[column];
    // Only all-digit codes are numbers. Each is converted to a number and back, and compared as text.
    if (!Regex.IsMatch(code, @"^\d+$"))
    {
        continue;
    }
    var back = long.Parse(code, CultureInfo.InvariantCulture).ToString(CultureInfo.InvariantCulture);
    if (back != code)
    {
        changed++;
    }
}
Console.WriteLine($"Postal codes that change: {changed}");
