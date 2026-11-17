// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package YamlDotNet@18.1.0

using YamlDotNet.Serialization;

var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "customers.yaml");
var customers = new DeserializerBuilder().IgnoreUnmatchedProperties().Build().Deserialize<List<Customer>>(File.ReadAllText(path));
var norwegian = customers.Count(customer => customer.country_code == "NO");
Console.WriteLine($"Norwegian customers: {norwegian}");

class Customer
{
    public string country_code { get; set; } = "";
}
