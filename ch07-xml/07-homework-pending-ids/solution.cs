// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

using System.Xml;
using System.Xml.Linq;

var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "orders.xml");
var settings = new XmlReaderSettings { DtdProcessing = DtdProcessing.Prohibit, XmlResolver = null };
using var reader = XmlReader.Create(path, settings);
var root = XDocument.Load(reader).Root;
var pending = new List<string>();
foreach (var order in root.Elements("order"))
{
    if (order.Element("status").Value == "pending")
    {
        // The identifier is an attribute, so it is read with Attribute, not Element.
        pending.Add(order.Attribute("id").Value);
    }
}
var idsText = string.Join(", ", pending);
Console.WriteLine($"Pending orders: {pending.Count}");
Console.WriteLine($"Pending ids: {idsText}");
