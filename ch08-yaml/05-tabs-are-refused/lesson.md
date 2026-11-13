# Tabs Are Refused

The file `config-yaml-tabs.yaml` has three lines. The second and third are indented with a tab character, not with spaces. In an editor that shows tabs as four spaces, the file looks correct. A YAML parser does not accept a tab for indentation, and it refuses the whole file.

The refusal is a feature. A file that looks right but parses differently is the dangerous case, and a parser that refuses it makes the problem visible at the line where it occurs. The sample below tries to load the file, and reports a refusal if the parser rejects it. It catches only the parser's own error, so a file that can't be opened still stops the program, as it should.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false
#:package YamlDotNet@18.1.0

// The sample file is read from the folder named by TRAINING_DATA. Only the parser's own error is caught.
using YamlDotNet.Core;
using YamlDotNet.Serialization;
var path = Path.Combine(Environment.GetEnvironmentVariable("TRAINING_DATA"), "config-yaml-tabs.yaml");
try
{
    new DeserializerBuilder().Build().Deserialize<Dictionary<string, object>>(File.ReadAllText(path));
    Console.WriteLine("Loaded: yes");
}
catch (YamlException)
{
    Console.WriteLine("Refused: the file is not valid YAML");
}
```
```python
import os

import yaml

# The sample file is read from the folder named by TRAINING_DATA. Only the parser's own error is caught.
path = os.path.join(os.environ["TRAINING_DATA"], "config-yaml-tabs.yaml")
with open(path, encoding="utf-8") as handle:
    text = handle.read()
try:
    yaml.safe_load(text)
    print("Loaded: yes")
except yaml.YAMLError:
    print("Refused: the file is not valid YAML")
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";
import { load } from "js-yaml";

// The sample file is read from the folder named by TRAINING_DATA. Only the parser's own error is caught.
const text = readFileSync(path.join(process.env.TRAINING_DATA, "config-yaml-tabs.yaml"), "utf8");
try {
  load(text);
  console.log("Loaded: yes");
} catch (error) {
  if (error.name !== "YAMLException") throw error;
  console.log("Refused: the file is not valid YAML");
}
```
~~~

The output is the same in every language:

~~~text
Refused: the file is not valid YAML
~~~

All three refuse the file, and all three report the same thing. The message says what happened, not where, so the parser's own line and column are the next thing to look at. Each library reports its own error text, and the sample doesn't print it, for the same reason as the XML entity sample: the wording belongs to the library and changes between versions.

The catch is narrow on purpose. The C# and Python samples catch the library's base error type, and the JavaScript sample checks the error's name and rethrows anything else. A missing file, a permission error, or a bug in the program is not a refusal, and it should not be reported as one.

> **Aside: a tab is fine inside a value.**
> YAML forbids tabs for indentation, not inside a quoted or plain value. A tab in a name is ordinary text, and the same tab used as indentation is the error.

> **Common mistake.** Converting tabs to spaces by search and replace across the whole file, including inside values. A value such as `"Name\tOther"` changes, and the change is silent. Convert only the leading indentation.

---
