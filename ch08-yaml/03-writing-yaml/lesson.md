# Writing YAML

Writing YAML turns a value into text that another program can read back. Each library has its own layout: where the indentation goes, how a list is shown under a key, and which strings it quotes. Those choices are cosmetic, so a file written by one library and read by another is the same data, as long as the reader follows the same version of YAML. The useful test is the round trip: write the record, read it back, and compare.

The sample below does that for one customer typed into the code. The customer's country code is `NO`, which is the value that an older YAML reader treats as a boolean. The sample writes the record, reads it back with the safe loader, and reports whether the name, the country code, and the tags are the same as before. The output is the round-trip result, not the YAML text, because the text differs between libraries.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package YamlDotNet@18.1.0

// Inline data, not from a sample file. One customer, typed into the code, with the country code NO and a list of tags.
using System.Collections;
using YamlDotNet.Serialization;
var record = new Dictionary<string, object>
{
    ["customer_id"] = 1002,
    ["name"] = "Okafor, Chidi",
    ["country_code"] = "NO",
    ["tags"] = new List<string> { "vip", "newsletter" },
};
var yaml = new SerializerBuilder().Build().Serialize(record);
var back = new DeserializerBuilder().Build().Deserialize<Dictionary<string, object>>(yaml);
var tags = (IList)back["tags"];
var matches = back["name"].ToString() == "Okafor, Chidi" && back["country_code"].ToString() == "NO" && tags.Count == 2;
var answer = matches ? "yes" : "no";
Console.WriteLine($"Round trip matches: {answer}");
```
```python
import yaml

# Inline data, not from a sample file. One customer, typed into the code, with the country code NO and a list of tags.
record = {"customer_id": 1002, "name": "Okafor, Chidi", "country_code": "NO", "tags": ["vip", "newsletter"]}
text = yaml.safe_dump(record, sort_keys=False)
back = yaml.safe_load(text)
matches = back == record
print(f"Round trip matches: {'yes' if matches else 'no'}")
```
```javascript
import { dump, load } from "js-yaml";

// Inline data, not from a sample file. One customer, typed into the code, with the country code NO and a list of tags.
const record = { customer_id: 1002, name: "Okafor, Chidi", country_code: "NO", tags: ["vip", "newsletter"] };
const text = dump(record);
const back = load(text);
const matches = JSON.stringify(back) === JSON.stringify(record);
console.log(`Round trip matches: ${matches ? "yes" : "no"}`);
```
~~~

The output is the same in every language:

~~~text
Round trip matches: yes
~~~

The round trip is the check to rely on. Each writer produced different text, and each one read back to the same data. Some writers quote `NO` and others leave it bare. The bare form reads back correctly under the YAML 1.2 rules that `js-yaml` uses, but an older reader that follows YAML 1.1 would read it as a boolean. The next step shows that difference.

The round trip also checks the things a written file most often gets wrong: a comma inside a name, a list under a key, and a value that looks like another type. A comparison of the text against an expected string would fail on a harmless change in layout, so the sample compares the data.

> **Aside: the layout is not the data.**
> Two files can have different indentation, quoting, and key order and still hold the same data. A test that compares text is testing the library's layout, and a round trip tests what the file means.

> **Common mistake.** Writing YAML by joining strings with indentation. A value that needs quoting, such as one containing a colon, is then written bare, and the reader sees a different structure. Let the library write the document.

---
