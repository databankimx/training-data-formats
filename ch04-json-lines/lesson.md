# 4. JSON Lines

JSON Lines puts one JSON value on each line of a file. It's the format of choice for logs, event streams, and exports too large to hold as one array, because each line can be read, checked, and written on its own. A single bad line costs one record, not the whole file. That is the property this chapter is about.

## What the format looks like

These are the first two lines of `customers.jsonl`, with some fields left out. Each line is one complete customer, and the `...` marks the fields that are not shown. The file has no brackets around it and no commas between the lines, and the other ten customers follow in the same way.

```json
{"customer_id": 1001, "name": "Alice Carter", "active": true, ...}
{"customer_id": 1002, "name": "Okafor, Chidi", "active": false, ...}
```

The chapter covers what the format is and how it differs from a JSON array, reading the file one line at a time, writing it, and what to do with a line that won't parse. Two sample files do the work. `customers.jsonl` holds the twelve customers, one per line. `orders-lines.jsonl` holds the twenty-four orders, and its seventh line is cut short, so it's malformed.

The chapter has a reading step, three samples, two homework items, and a summary with three quizzes.

**Libraries.** No third-party packages. C# uses `System.IO`, for `StreamReader`, and `System.Text.Json`, both part of the .NET base libraries. Python uses `json` and `os`, both from the standard library. JavaScript uses the built-in `JSON` object, plus `node:fs`, `node:path`, and `node:readline`, all built into Node.

---
