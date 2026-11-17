// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package ClosedXML@0.105.1

using System.Globalization;
using ClosedXML.Excel;

var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers.xlsx");
using var workbook = new XLWorkbook(path);
var rows = workbook.Worksheet("customers").RowsUsed().Skip(1).ToList();
var active = 0;
// decimal keeps each balance exact. The stored double is converted once, at a precision that holds the cents.
decimal total = 0;
foreach (var row in rows)
{
    if (row.Cell(6).GetValue<bool>())
    {
        active++;
    }
    total += decimal.Round((decimal)row.Cell(5).GetValue<double>(), 2);
}
var totalText = total.ToString("F2", CultureInfo.InvariantCulture);
Console.WriteLine($"Active customers: {active}");
Console.WriteLine($"Total balance: {totalText}");
