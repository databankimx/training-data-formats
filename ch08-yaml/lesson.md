# 8. YAML

YAML is the format people write by hand. Configuration files, deployment manifests, and test fixtures use it because it reads cleanly: structure comes from indentation, and most values need no punctuation. That convenience has a cost. YAML decides types from the text, so an unquoted value can change meaning, and an unsafe loader can run code that a file asks for. This chapter covers the structure, reading and writing, the way YAML decides a value's type, and a file that uses tabs, which the format refuses.

The sample file is `customers.yaml`, which holds the twelve customers. A second file, `config-norway.yaml`, shows the type problem, and `config-yaml-tabs.yaml` shows a file the parser refuses. Here is the start of `customers.yaml`, shortened, with `...` marking the omitted fields and customers:

```yaml
- customer_id: 1001
  name: Alice Carter
  email: alice.carter@example.invalid
  signup_date: '2021-03-14'
  balance: '1250.75'
  active: true
  country_code: US
  address:
    street: 12 Maple Street
    city: Springfield
    postal_code: '62704'
  tags: ...
- ...
```

The document is a list, and each list item is a mapping. Indentation is the structure, and it must be spaces. The dates and the balance are quoted, because the writer quoted them, and a quoted value stays text in every reader.

**Libraries.** C# uses YamlDotNet 18.1.0 (MIT, with an MIT-licensed libyaml component), declared in each sample with a `#:package` line, along with `System.IO` and `System.Linq`. Python uses PyYAML 6.0.3 (MIT) and `os`. JavaScript uses `js-yaml` 5.4.1 (MIT, with a PSF-licensed dependency that you have approved), declared in `samples\package.json`, along with `node:fs` and `node:path`. Install the JavaScript packages with `npm install` in `samples` before running the JavaScript samples.

The chapter has a reading step, four samples, two homework items, and a summary with three quizzes.

---
