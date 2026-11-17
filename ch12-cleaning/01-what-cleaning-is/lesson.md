# What Cleaning Is

A cleaner has four kinds of decision for each value. It can change a value when the change is certain, such as removing spaces around a name. It can leave a value alone when it is already correct. It can refuse to change a value and report it, when the fix needs knowledge the cleaner doesn't have. And it can remove a row, which is the most serious of the four, and should happen only when the copy is exactly the same as a copy that is kept.

The dividing line is certainty. `14/03/2021` is certainly day-first, because there is no fourteenth month. `03/04/2021` is not certainly anything: it could be the third of April or the fourth of March, and a cleaner that picks one has invented a fact. The same reasoning applies to a null. A cleaner can decide that a null tags list means no tags, because that's the meaning the file gives it. It can't decide what a null email should be, because nothing in the data says.

Each change should be recorded with the row, the column, the old value, and the new value, or the reason no change was made. A cleaned file with no record of what changed can't be checked, and a person who finds a wrong value later has no way to trace it. The samples in this chapter print that record, one line for each change, so the rule and its effect can be read together.

Removing a row needs the strictest test. Two rows are duplicates only when every field matches, or when the rule for the file says a field is not significant. A copy with a different balance is not a duplicate. It's a conflict, and both copies must be kept until a person decides which is right.

> **Aside: cleaning is a change to the data, not a fix to the file.**
> The original file should never be overwritten. The cleaned result is written beside it, with its record, so the original can always be read again.

> **Common mistake.** Making every value pass by filling it with a default. A default such as `1900-01-01` for a missing date passes the schema, and it then reports a real date that never existed. A default is a fact, and it should be a fact the data supports.

---
