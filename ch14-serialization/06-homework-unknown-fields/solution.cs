// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

using System.Text.Json;

// Inline data, not from a sample file. Three records, typed into the code, with fields the record type does not declare.
var text = "[{\"customer_id\":1,\"name\":\"Ana Silva\",\"loyalty_points\":5},{\"customer_id\":2,\"name\":\"Ben Osei\",\"referrer\":\"1\",\"tier\":\"gold\"},{\"customer_id\":3,\"name\":\"Cara Dunn\"}]";
var known = new HashSet<string> { "customer_id", "name" };
using var document = JsonDocument.Parse(text);
var records = document.RootElement.GetArrayLength();
var unknown = 0;
foreach (var record in document.RootElement.EnumerateArray())
{
    foreach (var property in record.EnumerateObject())
    {
        if (!known.Contains(property.Name))
        {
            unknown++;
        }
    }
}
Console.WriteLine($"Records: {records}");
Console.WriteLine($"Unknown fields: {unknown}");
