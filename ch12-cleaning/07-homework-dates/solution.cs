// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

using System.Globalization;
using System.Text.RegularExpressions;

// Inline data, not from a sample file. Four dates in mixed forms.
var dates = new[] { "03/04/2021", "14/03/2021", "2021-3-4", "2021-03-04" };
var changed = 0;
var review = 0;
foreach (var date in dates)
{
    var iso = Regex.Match(date, @"^(\d{4})-(\d{1,2})-(\d{1,2})$");
    var slash = Regex.Match(date, @"^(\d{2})/(\d{2})/(\d{4})$");
    if (iso.Success && iso.Groups[2].Value.Length == 2 && iso.Groups[3].Value.Length == 2)
    {
        // Already in the ISO form. It is unchanged when it is a real date, and otherwise it needs review.
        if (!DateTime.TryParseExact(date, "yyyy-MM-dd", CultureInfo.InvariantCulture, DateTimeStyles.None, out _)) review++;
        continue;
    }
    if (slash.Success)
    {
        var first = int.Parse(slash.Groups[1].Value);
        if (first > 12)
        {
            changed++;
        }
        else
        {
            review++;
        }
        continue;
    }
    if (iso.Success)
    {
        var padded = $"{iso.Groups[1].Value}-{int.Parse(iso.Groups[2].Value):D2}-{int.Parse(iso.Groups[3].Value):D2}";
        if (DateTime.TryParseExact(padded, "yyyy-MM-dd", CultureInfo.InvariantCulture, DateTimeStyles.None, out _))
        {
            changed++;
        }
        else
        {
            review++;
        }
    }
}
Console.WriteLine($"Changed dates: {changed}");
Console.WriteLine($"Dates needing review: {review}");
