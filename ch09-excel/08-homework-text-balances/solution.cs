// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package ClosedXML@0.105.1

using System.Globalization;
using ClosedXML.Excel;

var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers-text-numbers.xlsx");
using var workbook = new XLWorkbook(path);
var rows = workbook.Worksheet("customers").RowsUsed().Skip(1).ToList();
var textCount = 0;
// decimal keeps each converted balance exact.
decimal total = 0;
foreach (var row in rows)
{
    var cell = row.Cell(5);
    if (cell.DataType == XLDataType.Text)
    {
        textCount++;
    }
    total += decimal.Parse(cell.GetString(), CultureInfo.InvariantCulture);
}
var totalText = total.ToString("F2", CultureInfo.InvariantCulture);
Console.WriteLine($"Text balances: {textCount}");
Console.WriteLine($"Text total: {totalText}");
