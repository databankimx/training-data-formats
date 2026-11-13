// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// The runtime needs this registration before it can decode Windows-1252.
System.Text.Encoding.RegisterProvider(System.Text.CodePagesEncodingProvider.Instance);
var folder = Environment.GetEnvironmentVariable("TRAINING_DATA");
var data = File.ReadAllBytes(Path.Combine(folder, "customers-windows-1252.csv"));
var text = System.Text.Encoding.GetEncoding(1252).GetString(data);
// Split into lines, then count the lines that contain the letter e-acute (U+00E9).
var count = text.Split('\n').Count(line => line.Contains('\u00e9'));
Console.WriteLine($"Lines containing e-acute: {count}");
