# What YAML Is

YAML has three shapes. A mapping is a set of keys and values, written as `key: value`. A sequence is an ordered list, with each item starting with a dash. A scalar is a single value. Nesting is shown by indentation, and the indentation must be spaces, because a tab is not allowed where the parser expects indentation. A file can hold several documents, separated by `---`, and a document can be a mapping, a sequence, or a scalar on its own.

Most of the work is in scalars. A plain scalar, one with no quotes, has its type decided by the reader from the text. `true`, `false`, numbers, `null`, and dates are recognised, and a reader that follows the YAML 1.1 rules also reads words such as `yes`, `no`, `on`, and `off` as booleans. A value written in quotes is always a string, whatever it contains. That's why the writer quoted the dates and the balance in `customers.yaml`: the file holds text, and a reader must not turn it into a date or a number.

The version of YAML matters. YAML 1.1 is older and recognises more words as booleans. YAML 1.2 is closer to JSON and reads only `true` and `false`. The two disagree about country codes such as `NO`, which is Norway, and the next sample shows the difference. A library's default is a choice, and the libraries here make different ones.

YAML is also a loading risk. In some libraries, a file can name a type, and the loader creates an object of that type, which can run code. The safe loader only builds plain values such as strings, numbers, lists, and maps. This chapter's samples use the safe settings of each library, and the rule applies to any YAML from outside your system: load it with the safe loader, and never with one that builds arbitrary types.

Tabs are the other trap. A tab can appear inside a value, but YAML refuses a tab used for indentation. A file that looks correct in an editor, where the tab is shown as a few spaces, is refused by the parser, and the error points at a line that seems fine. The fifth sample shows the refusal.

> **Aside: the same text, two readings.**
> A value such as `no` means one thing to a reader that follows YAML 1.1, and another to a reader that follows YAML 1.2. A file written for one reader can be read wrongly by the other, with no error from either.

> **Common mistake.** Writing a config value without quotes because it looks harmless. `NO`, `on`, `2021-03-14`, and `1.10` all change type on some readers. Quote any value you want kept as it is.

---
