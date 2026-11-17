// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

using System.Globalization;
using System.Xml;
using System.Xml.Linq;

var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "orders.xml");
var settings = new XmlReaderSettings { DtdProcessing = DtdProcessing.Prohibit, XmlResolver = null };
using var reader = XmlReader.Create(path, settings);
var root = XDocument.Load(reader).Root;
var shipped = 0;
// decimal keeps each amount exact, so the total has no floating-point drift.
decimal total = 0;
foreach (var order in root.Elements("order"))
{
    if (order.Element("status").Value == "shipped")
    {
        shipped++;
        total += decimal.Parse(order.Element("amount").Value, CultureInfo.InvariantCulture);
    }
}
var totalText = total.ToString("F2", CultureInfo.InvariantCulture);
Console.WriteLine($"Shipped orders: {shipped}");
Console.WriteLine($"Shipped total: {totalText}");
