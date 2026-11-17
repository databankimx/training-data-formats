# 17. Testing With Fixtures

Every chapter in this tutorial has checked its samples against an expected output, and the same idea applies to a data program. A test runs the program on a known input and compares the result with a known answer. The known input is a fixture, and the known answer is its expected result. A program that passes its fixtures has shown that it does what the fixtures say, for those cases. It has not shown that it is correct in general, and the chapter is careful about that difference.

Three kinds of test cover most of the data work in this tutorial. A round-trip test writes data out and reads it back, and checks that nothing changed, as the serialization and conversion chapters did. A golden-file test compares the output of a program with a stored expected output, and fails when the output changes. A refusal test checks that bad input is rejected, as the validation and security chapters required.

The chapter's samples use plain checks that print a pass or a fail, so the results are visible without a test framework. Python and JavaScript both ship a test runner in the standard library and in Node, and a real project would use one. The checks written here are the same checks, and moving them into a runner changes only where the pass and fail are reported.

**Libraries.** No new libraries. C# uses `System.IO`, `System.Text.Json`, and `System.Linq`, with plain checks in the program. Python uses the standard `json`, `os`, and `csv` modules. JavaScript uses `node:fs`, `node:path`, `node:assert`, and the built-in `JSON` object.

The chapter has a reading step, three samples, two homework items, and a summary with three quizzes.

---
