// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

var folder = Environment.GetEnvironmentVariable("TRAINING_DATA");
var names = new[] { "customers.parquet", "customers.xlsx", "customers-as-json.csv" };
foreach (var name in names)
{
    var data = File.ReadAllBytes(Path.Combine(folder, name));
    Console.WriteLine($"{name}: {Kind(data)}");
}

// Checks the signatures in order, and returns the first kind that matches.
string Kind(byte[] data)
{
    if (StartsWith(data, "PAR1")) return "parquet";
    if (StartsWith(data, "PK\u0003\u0004")) return "zip";
    if (StartsWith(data, "\u00d0\u00cf\u0011\u00e0\u00a1\u00b1\u001a\u00e1")) return "ole2";
    var start = 0;
    while (start < data.Length && (data[start] == (byte)' ' || data[start] == (byte)'\t' || data[start] == (byte)'\r' || data[start] == (byte)'\n'))
    {
        start++;
    }
    if (start < data.Length && (data[start] == (byte)'[' || data[start] == (byte)'{')) return "json";
    if (StartsWith(data, "<?xml")) return "xml";
    if (Array.IndexOf(data, (byte)0) >= 0) return "binary";
    return "text";
}

bool StartsWith(byte[] data, string text)
{
    if (data.Length < text.Length) return false;
    for (var i = 0; i < text.Length; i++)
    {
        if (data[i] != (byte)text[i]) return false;
    }
    return true;
}
