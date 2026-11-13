// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

using System.Globalization;

var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers.fixed");
var lines = File.ReadAllLines(path, System.Text.Encoding.UTF8);
var active = 0;
var largestText = "";
var largest = decimal.MinValue;
foreach (var line in lines)
{
    // The active flag is at positions 49 to 53, and the balance at positions 40 to 47.
    if (line.Substring(48, 5).Trim() == "true")
    {
        active++;
    }
    var balanceText = line.Substring(39, 8).Trim();
    var balance = decimal.Parse(balanceText, CultureInfo.InvariantCulture);
    if (balance > largest)
    {
        largest = balance;
        largestText = balanceText;
    }
}
Console.WriteLine($"Active customers: {active}");
Console.WriteLine($"Largest balance: {largestText}");
