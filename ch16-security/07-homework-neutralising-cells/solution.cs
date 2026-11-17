// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

using System.Globalization;

// Inline data, not from a sample file. Four cell values, typed into the code, from a file someone else sent.
var values = new[] { "=1+1", "Alice", "-45.00", "@SUM(A1)" };
var formulaStarts = new[] { '=', '+', '-', '@' };
var neutralised = 0;
var leftAlone = 0;
foreach (var value in values)
{
    var isNumber = decimal.TryParse(value, NumberStyles.Float, CultureInfo.InvariantCulture, out _);
    if (value.Length > 0 && formulaStarts.Contains(value[0]) && !isNumber)
    {
        neutralised++;
    }
    else
    {
        leftAlone++;
    }
}
Console.WriteLine($"Neutralised: {neutralised}");
Console.WriteLine($"Left alone: {leftAlone}");
