// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

var folder = Environment.GetEnvironmentVariable("TRAINING_DATA");
var names = new[] { "customers-utf8-bom.csv", "customers-windows-1252.csv", "config-norway.yaml" };
foreach (var name in names)
{
    var data = File.ReadAllBytes(Path.Combine(folder, name));
    // The mark is checked on the bytes, before anything is decoded.
    var hasMark = data.Length >= 3 && data[0] == 0xEF && data[1] == 0xBB && data[2] == 0xBF;
    var suffix = hasMark ? ", with byte-order mark" : "";
    // A file with no NUL byte is text. The mark doesn't change that.
    var kind = Array.IndexOf(data, (byte)0) >= 0 ? "binary" : "text";
    Console.WriteLine($"{name}: {kind}{suffix}");
}
