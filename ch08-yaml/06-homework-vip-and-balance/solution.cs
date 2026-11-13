// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package YamlDotNet@18.1.0

using System.Globalization;
using YamlDotNet.Serialization;

var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers.yaml");
var customers = new DeserializerBuilder().IgnoreUnmatchedProperties().Build().Deserialize<List<Customer>>(File.ReadAllText(path));
var vip = 0;
// decimal keeps each balance exact, so the total has no floating-point drift.
decimal total = 0;
foreach (var customer in customers)
{
    if (customer.tags.Contains("vip"))
    {
        vip++;
    }
    total += decimal.Parse(customer.balance, CultureInfo.InvariantCulture);
}
var totalText = total.ToString("F2", CultureInfo.InvariantCulture);
Console.WriteLine($"VIP customers: {vip}");
Console.WriteLine($"Total balance: {totalText}");

class Customer
{
    public string balance { get; set; } = "";
    public List<string> tags { get; set; } = new List<string>();
}
