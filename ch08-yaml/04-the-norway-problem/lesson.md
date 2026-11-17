# The Norway Problem

The file `config-norway.yaml` lists two countries and a notifications setting. Its country code is `NO`, which is Norway's ISO code, and its notifications setting is `on`. Neither is quoted. The problem is that YAML 1.1 treats `NO` as the boolean false and `on` as the boolean true. A reader that follows YAML 1.1 turns the country code into `False` and the setting into `True`, and nothing reports the change.

The sample below reads the file and prints the first country's code and the notifications setting. Each library follows a different version of YAML, or a different choice about types, and the output shows which.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package YamlDotNet@18.1.0

// The sample file is read from the folder named by TRAINING_DATA. The values are read into typed string properties.
using YamlDotNet.Serialization;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "config-norway.yaml");
var config = new DeserializerBuilder().Build().Deserialize<Config>(File.ReadAllText(path));
Console.WriteLine($"Country code: {config.countries[0].code}");
Console.WriteLine($"Notifications: {config.settings.notifications}");

class Config
{
    public List<Country> countries { get; set; } = new List<Country>();
    public Settings settings { get; set; } = new Settings();
}

class Country
{
    public string code { get; set; } = "";
    public string name { get; set; } = "";
}

class Settings
{
    public string notifications { get; set; } = "";
    public string retry { get; set; } = "";
}
```
```python
import os

import yaml

# The sample file is read from the folder named by TRAINING_DATA. PyYAML follows YAML 1.1, where NO and on are booleans.
path = os.path.join(os.environ["TRAINING_DATA"], "config-norway.yaml")
with open(path, encoding="utf-8") as handle:
    config = yaml.safe_load(handle)
print(f"Country code: {config['countries'][0]['code']}")
print(f"Notifications: {config['settings']['notifications']}")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";
import { load } from "js-yaml";

// The sample file is read from the folder named by TRAINING_DATA. js-yaml's default schema follows YAML 1.2, where NO and on are plain text.
const config = load(readFileSync(path.join(process.env.TRAINING_DATA, "config-norway.yaml"), "utf8"));
console.log(`Country code: ${config.countries[0].code}`);
console.log(`Notifications: ${config.settings.notifications}`);
```
~~~

The output differs by language. Each block below is the output of one language:

~~~text
C#:
Country code: NO
Notifications: on

Python:
Country code: False
Notifications: True

JavaScript:
Country code: NO
Notifications: on
~~~

The PyYAML output is the problem in full. The country code has become `False`, and the notifications setting has become `True`. The C# and JavaScript outputs keep the text, because C# is given string properties to fill and js-yaml follows YAML 1.2 by default. Neither of those is a guarantee for every reader. The text in the file is ambiguous, and only the reader's version decides what it means.

The fix is in the file, not the reader. Quoting the values, as `'NO'` and `'on'`, makes them strings in every version of YAML. Writers that produce YAML for other systems should quote any value that a reader might treat as a boolean, a null, or a number.

> **Aside: a country code is a string, always.**
> The code `NO` identifies a country. The same is true of other codes that look like keywords, such as `ON` for Ontario, which is a code in some systems. A value that identifies something should be a string in the file and in the program.

> **Common mistake.** Testing a reader only with values that are obviously strings, such as names. The Norway code passes through a name-based test unchanged, and fails only when a code happens to match a keyword.

---
