// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

using System.Text.RegularExpressions;

// Inline data, not from a sample file. Name, country code, and email for three customers.
var records = new[]
{
    (name: "  Alice   Carter ", country: "us", email: "alice@example.invalid"),
    (name: "Chidi Okafor", country: "GB", email: ""),
    (name: "Mei\u00A0Lin", country: "SG", email: "mei@example.invalid"),
};
var changed = 0;
var review = 0;
foreach (var record in records)
{
    var name = Regex.Replace(record.name, @"\s+", " ").Trim();
    if (name != record.name) changed++;
    var country = record.country.Trim().ToUpperInvariant();
    if (country != record.country) changed++;
    if (record.email == "") review++;
}
Console.WriteLine($"Changed values: {changed}");
Console.WriteLine($"Values needing review: {review}");
