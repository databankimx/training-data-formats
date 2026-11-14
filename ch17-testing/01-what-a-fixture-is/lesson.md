# What a Fixture Is

A fixture is a fixed input with a known result, and the test is the comparison between the program's output and that result. The fixture is chosen to exercise one behaviour, so a failure points at a cause. A fixture that tests everything at once tells you that something is wrong, not what.

A test has three parts. The arrange step sets up the input, which is the fixture. The act step runs the program on it. The assert step compares the result with the expected value, and reports a pass or a fail. The expected value is written down before the program runs, and it should come from somewhere other than the program. If the expected value is produced by running the program, the test checks that the program is consistent with itself, and that is not the same as checking that it is right.

The chapter uses three kinds of test. A round-trip test writes a value out and reads it back, and checks that the value is the same. The test does not need to know the format, only that the two directions agree. A golden-file test compares the output with a stored text, the golden file, and fails when the output differs. Golden files are useful for output that is long, but they must be reviewed when they change, because a changed golden file that nobody reads will be accepted without thought. A refusal test checks that bad input is rejected, and that the rejection is the one expected, not some other failure.

A passing test proves that the program does what the fixtures say, for the cases the fixtures cover. It does not prove the program is correct for every input, and a test suite with a single fixture can pass while the program is wrong for most of its inputs. The number and variety of the fixtures is the measure of the coverage, and a fixture that covers only the easy case is a weak test.

> **Aside: a test that cannot fail is not a test.**
> Before trusting a test, check that it fails when the program is wrong. Change the expected value on purpose, or break the program, and confirm the test reports a failure.

> **Common mistake.** Writing the expected value by copying the program's output. The test then passes whatever the program does, including when it is wrong. Derive the expected value by hand or from a source that does not run the program.

---
