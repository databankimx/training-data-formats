# How the Samples Read Data

The sample files live in one folder, `samples\data`, next to the tutorial. The runner tells every sample where that folder is, through an environment variable called `TRAINING_DATA`. A sample never has a path written into it. It builds the path from `TRAINING_DATA` and the file name, so the same sample works in the runner, in the lesson, and on your own machine after you copy the folder.

The sample below opens `customers.csv` and prints its first line, which is the column names. Press Run in any tab. The three versions do the same thing, and print the same line.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// The sample file is read from the folder named by TRAINING_DATA. Nothing is typed in by hand.
var folder = Environment.GetEnvironmentVariable("TRAINING_DATA");
var path = Path.Combine(folder, "customers.csv");
using var reader = new StreamReader(path, System.Text.Encoding.UTF8);
Console.WriteLine(reader.ReadLine());
```
```python
import os

# The sample file is read from the folder named by TRAINING_DATA. Nothing is typed in by hand.
path = os.path.join(os.environ["TRAINING_DATA"], "customers.csv")
with open(path, encoding="utf-8", newline="") as handle:
    print(handle.readline().rstrip("\r\n"))
```
```javascript
import { readFileSync } from "node:fs";
import path from "node:path";

// The sample file is read from the folder named by TRAINING_DATA. Nothing is typed in by hand.
const file = path.join(process.env.TRAINING_DATA, "customers.csv");
const text = readFileSync(file, "utf8");
console.log(text.split("\n")[0].replace(/\r$/, ""));
```
~~~

The output is the same in every language:

~~~text
customer_id,name,email,signup_date,balance,active,country_code,address_street,address_city,address_postal_code,tags
~~~

Read the first line of output with the file open next to it. The first column is `customer_id`, and the last is `tags`. The line has eleven names, because the address is flattened into three columns, and the tags are joined with semicolons. CSV has no nesting, so the structure is lost on the way in. Chapter 5 returns to this.

## Inline data

Most samples in this tutorial read a sample file, as this one does. Some do not. A sample that types its data into the code, to show one specific byte or character, says so in a comment directly above the data. The comment begins "Inline data, not from a sample file." You will see it in Chapter 1, and it will appear in any later sample that does the same thing.

The rule exists so you always know where a sample's input came from. If a sample reads a file, the file is the input. If a comment says inline, the value on the line is the input, and it is the only input.

> **Aside: where is the path?**
> The sample never shows a full path such as `C:\Development\...`. The runner sets `TRAINING_DATA`, so the same code runs unchanged in any copy of the tutorial.

> **Common mistake.** Writing the path into the code, for example `C:\Development\training\training-data-formats\samples\data\customers.csv`. It works on your machine, and fails the first time the folder moves. Build the path from `TRAINING_DATA` instead.

---
