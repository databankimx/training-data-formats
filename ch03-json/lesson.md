# 3. JSON

JSON is the format most APIs speak, and most configuration files that aren't YAML. It's easy to read, which hides how much a parser decides for you: what a number is, whether a missing key and a null mean the same thing, and what happens to a value too large for the type your language uses. This chapter covers reading, writing, nested data, large integers, nulls, and a defective file. Each idea has its own sample, and the homework builds on them.

The sample files are in the data folder. `customers.json` holds the twelve customers as nested JSON, with an address object and a list of tags. Two of the other files are there to show the failures: `customers-big-numbers.json` holds integers too large for some readers, and `customers-null-mix.json` holds nulls, empty strings, and missing keys. A third, `customers-truncated.json`, is cut off partway through.

## What the format looks like

This is the first customer in `customers.json`, with some fields left out. The `...` lines mark the fields and the other eleven customers that are not shown.

```json
[
  {
    "customer_id": 1001,
    "name": "Alice Carter",
    "balance": 1250.75,
    "active": true,
    "address": {
      "street": "12 Maple Street",
      ...
    },
    "tags": [
      "vip",
      "newsletter"
    ]
  },
  ...
]
```

Notice the balance is written as `1250.75`, with no quotes, because it's a number. The types are part of the format, and the parser keeps them.

The chapter has a reading step, six samples, two homework items, and a summary with three quizzes.

**Libraries.** No third-party packages. C# uses `System.Text.Json`, which ships with .NET, for `JsonDocument` and `JsonSerializer`, along with `System.IO`. Python uses `json` and `os`, both from the standard library. JavaScript uses the built-in `JSON` object, plus `node:fs` and `node:path`.

---
