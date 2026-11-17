// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// Converts a balance's text to whole cents, splitting at the decimal point so no binary float is used.
long ToCents(string text)
{
    var parts = text.Split('.');
    var pounds = long.Parse(parts[0]);
    var cents = parts.Length > 1 ? long.Parse(parts[1].PadRight(2, '0')) : 0;
    return pounds * 100 + cents;
}

// Inline data, not from a sample file. Four cases, typed into the code, with the expected cents.
var cases = new[] { ("1250.75", 125075L), ("0.00", 0L), ("980.1", 98010L), ("4410", 441000L) };
var passed = 0;
var failed = 0;
foreach (var (input, expected) in cases)
{
    if (ToCents(input) == expected) passed++; else failed++;
}
Console.WriteLine($"Cases passed: {passed}");
Console.WriteLine($"Cases failed: {failed}");
