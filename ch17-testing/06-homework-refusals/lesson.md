# Homework: Refusals

The four inputs below are typed into the code, so the data is inline. Each one is sent to a JSON reader.

1. `[{"a":1}]`
2. `[{"a":`
3. the empty string
4. `{"a":1}`

A reader refuses an input when its parser reports an error, and accepts it when the parse succeeds. Only the parser's own error counts as a refusal, as the refusal test showed. Print two lines and nothing else:

1. `Refused: ` followed by the number of inputs refused.
2. `Accepted: ` followed by the number of inputs accepted.

The expected output is:

~~~text
Refused: 2
Accepted: 2
~~~

Check compares your output with that, and ignores line endings and trailing spaces.

Two of the inputs are refused, the truncated one and the empty one. An empty input is not a valid JSON document, and a test that refuses it for that reason is correct. The other two parse, so they are accepted. The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
