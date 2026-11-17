// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

var folder = Environment.GetEnvironmentVariable("TRAINING_DATA");
var data = File.ReadAllBytes(Path.Combine(folder, "customers-utf8-bom.csv"));
// The mark is the three bytes EF BB BF. Check the bytes first, then skip them before decoding.
var hasMark = data.Length >= 3 && data[0] == 0xEF && data[1] == 0xBB && data[2] == 0xBF;
var start = hasMark ? 3 : 0;
var text = System.Text.Encoding.UTF8.GetString(data, start, data.Length - start);
var header = text.Split('\n')[0].Split(',')[0];
var markText = hasMark ? "yes" : "no";
Console.WriteLine($"Starts with a byte-order mark: {markText}");
Console.WriteLine($"First header: {header}");
