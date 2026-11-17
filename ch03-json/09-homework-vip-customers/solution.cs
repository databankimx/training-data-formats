// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

using System.Text.Json;

var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers.json");
using var document = JsonDocument.Parse(File.ReadAllText(path, System.Text.Encoding.UTF8));
foreach (var customer in document.RootElement.EnumerateArray())
{
    // A VIP is a customer whose tags list contains "vip". The tags are checked one at a time.
    var isVip = false;
    foreach (var tag in customer.GetProperty("tags").EnumerateArray())
    {
        if (tag.GetString() == "vip")
        {
            isVip = true;
        }
    }
    if (isVip)
    {
        var id = customer.GetProperty("customer_id").GetInt64();
        var city = customer.GetProperty("address").GetProperty("city").GetString();
        Console.WriteLine($"{id} {city}");
    }
}
