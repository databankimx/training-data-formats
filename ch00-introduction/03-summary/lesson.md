# Summary: Introduction

This chapter set out what the tutorial covers, and how its samples find their data.

## What you learned

- Every format is worked through five jobs: reading, writing, cleaning, converting, and serializing and manipulating.
- All the good sample files describe the same twelve customers and twenty-four orders, so a conversion can be checked against the original.
- Some sample files are wrong on purpose, and each one is named for its failure. A bad file is never fixed in place.
- A sample builds its path from the TRAINING_DATA location, so the same sample runs in the runner, in the lesson, and on your own machine.
- A sample that types its data into the code says so in a comment, beginning "Inline data, not from a sample file."

## Quizzes

Three questions, one for each big idea in the chapter. Pick an answer, and read the explanation whichever way it goes.

```quiz
A sample needs the sample data folder. What should it do?
○ Write the full path, such as C:\Development\...\samples\data, into the code.
→ That works on one machine only. The path breaks as soon as the folder moves.
◉ Build the path from TRAINING_DATA and the file name.
→ Right. The runner supplies TRAINING_DATA, so the same code runs in any copy of the tutorial.
○ Search the whole disk for a file with that name.
→ A search is slow, and it can find the wrong file. The runner gives the exact location.
```

```quiz
A sample prints a value that doesn't come from any file. What must its code say?
◉ A comment, directly above the data, beginning "Inline data, not from a sample file."
→ Right. The comment tells the reader where the input came from.
○ Nothing, because the tutorial is trusted.
→ The rule exists so that every sample says where its input came from, including this tutorial's own samples.
○ A note at the end of the lesson, outside the code.
→ The note can be missed. The comment belongs in the code, beside the data.
```

```quiz
Which statement about the sample dataset is true?
○ Each good file holds different customers, so the files can be compared.
→ The good files share one dataset. That is what makes a conversion checkable.
○ The bad files are corrected copies of the good ones.
→ Bad files are never fixed in place. Your code deals with them, and the lesson shows what the fix does.
◉ The good files all hold the same twelve customers and twenty-four orders.
→ Right. A value that goes missing in a conversion shows up as a difference from the dataset.
```

---
