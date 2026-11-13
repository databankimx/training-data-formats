// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

var folder = Environment.GetEnvironmentVariable("TRAINING_DATA");
var data = File.ReadAllBytes(Path.Combine(folder, "customers-mixed-line-endings.csv"));
// Every LF is one line. A CRLF is an LF with a carriage return before it.
var lineFeeds = 0;
var crlf = 0;
for (var i = 0; i < data.Length; i++)
{
    if (data[i] == (byte)'\n')
    {
        lineFeeds++;
        if (i > 0 && data[i - 1] == (byte)'\r')
        {
            crlf++;
        }
    }
}
Console.WriteLine($"Lines: {lineFeeds}");
Console.WriteLine($"CRLF: {crlf}");
Console.WriteLine($"LF only: {lineFeeds - crlf}");
