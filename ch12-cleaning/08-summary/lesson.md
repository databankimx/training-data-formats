# Summary: Cleaning

This chapter covered cleaning: changes that are made only when their meaning is certain, reports for the rest, and a record of every decision.

## What you learned

- A cleaner changes a value only when the change is certain. A value it can't decide goes to review, with the reason.
- Whitespace is cleaned by trimming the ends and collapsing runs inside a value, and a non-breaking space is whitespace too.
- A slash date whose first part is greater than twelve is day first. A date with a month name is converted only when the month is known. A date with both parts twelve or less is ambiguous, and it goes to review.
- A null is replaced only where the data defines its meaning, such as a null tags list meaning no tags. Other nulls and empty values go to review.
- A repeated row is removed only when every field matches. A repeat that differs is kept and flagged.
- The original file is never overwritten, and every change is recorded with its reason.

## Quizzes

Three questions, one for each big idea in the chapter. Pick an answer, and read the explanation whichever way it goes.

```quiz
A date in a file is 03/04/2021. Which decision is correct?
○ Convert it as day first, because the first part is the day in most of the world.
→ The data itself does not say which part is the day, so the choice is a guess.
◉ Send it to review, because both parts are twelve or less, so either reading is possible.
→ Right. The cleaner has no basis for choosing, so the decision belongs to a person.
○ Convert it as month first, because the file is in a US format.
→ Nothing in the file says the format is US, so this is another guess.
```

```quiz
Two rows have the same identifier. One has a different balance. What is the right treatment?
○ Remove the second row, because the identifier is the same.
→ The identifier alone does not make a row a duplicate. The balance differs, so the rows conflict.
○ Keep the first row and discard the second, with no record.
→ A removal with no record can't be checked, and it may discard the correct balance.
◉ Keep both rows and flag the second for review, because the rows conflict.
→ Right. Only a person can decide which balance is current, so the cleaner keeps both.
```

```quiz
A tags value is null in a record. What should the cleaner do?
◉ Replace it with an empty list, because the data gives a null tags value the meaning no tags.
→ Right. The replacement follows a rule the data supports, and it is recorded.
○ Replace it with an empty string, so the field passes a text check.
→ An empty string is a value that hides the null, and it is no better than a guess.
○ Remove the record, because a null tags value means the record is incomplete.
→ The record may be correct, and removing it discards good data.
```

---
