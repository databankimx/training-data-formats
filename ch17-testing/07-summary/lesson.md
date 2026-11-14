# Summary: Testing With Fixtures

This chapter covered tests for data programs: a fixture, an expected value, and a check that compares them.

## What you learned

- A fixture is a known input with a known result, and each test should exercise one behaviour.
- The expected value must come from somewhere other than the program. An expected value copied from the program's output tests nothing.
- A round-trip test writes a value out, reads it back, and checks each field.
- A golden-file test compares the output with a stored text, and a changed golden file needs a reviewer before it is accepted.
- A refusal test checks both sides of the boundary: that bad input is refused, and that good input is accepted.
- A test must be able to fail. A comparison that cannot report a difference proves nothing when it passes.

## Quizzes

Three questions, one for each big idea in the chapter. Pick an answer, and read the explanation whichever way it goes.

```quiz
A test's expected value is produced by running the program and saving its output. What does a passing test show?
○ That the program is correct, because the saved output was produced by the program.
→ The program agrees with its own output, which proves nothing about whether that output is right.
◉ That the program is consistent with its saved output, but not that the output is correct.
→ Right. The expected value must come from somewhere the program did not produce, or the test checks nothing.
○ That the golden file is out of date, because the program has changed.
→ A passing test shows agreement, not that the file is stale.
```

```quiz
A refusal test passes because the reader refuses every input, including good ones. What is missing from the test?
◉ A check that a complete, valid file is accepted, so the test shows the boundary is in the right place.
→ Right. Refusal and acceptance are both needed, and together they show the reader can tell them apart.
○ A check that a missing file is reported, because that is the only failure a reader can have.
→ A missing file is a different case. The gap is a check on the other side of the boundary.
○ A check that the refused file is named in the error message.
→ The message is useful, but the missing check is on acceptance, which proves the reader is not refusing everything.
```

```quiz
A golden-file test fails after a change to the program. What is the right first step?
○ Update the golden file to the new output, so that the test passes again.
→ That makes the test agree with the change before anyone has checked the change.
○ Delete the golden file, because a test that fails was wrong to be written.
→ A failing golden test has found a change. The golden file should not be deleted to hide it.
◉ Review the change to decide whether it is correct, and update the golden file only if it is.
→ Right. The golden file records what is judged correct, so a person decides before it changes.
```

---
