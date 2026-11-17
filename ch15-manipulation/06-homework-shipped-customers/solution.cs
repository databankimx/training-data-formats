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
var header = rows[0];
var customerIds = new HashSet<string>();
// decimal keeps each amount exact, so the total has no floating-point drift.
decimal total = 0;
foreach (var row in rows.Skip(1))
{
    if (row[Array.IndexOf(header, "status")] == "shipped")
    {
        customerIds.Add(row[Array.IndexOf(header, "customer_id")]);
        total += decimal.Parse(row[Array.IndexOf(header, "amount")], CultureInfo.InvariantCulture);
    }
}
var totalText = total.ToString("F2", CultureInfo.InvariantCulture);
Console.WriteLine($"Customers with a shipped order: {customerIds.Count}");
Console.WriteLine($"Shipped total: {totalText}");
