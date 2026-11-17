# Homework: Dates in Mixed Forms

The four dates below are typed into the code, so the data is inline. Apply the rules from the Fixing Dates step, in this order, and print two counts.

1. A date already in the ISO form, `YYYY-MM-DD`, that is a real date is unchanged.
2. A date with three parts separated by slashes, `DD/MM/YYYY`, whose first part is greater than twelve is converted to the ISO form, because the first part must be the day.
3. A date with a year, a month, and a day separated by dashes, where the month or day has one digit, is converted to the ISO form with two digits for each part, when the result is a real date.
4. A date with two slash parts that are both twelve or less is ambiguous. It needs review, and it is never converted.

The dates are `03/04/2021`, `14/03/2021`, `2021-3-4`, and `2021-03-04`.

Print two lines and nothing else:

1. `Changed dates: ` followed by the number of dates the rules converted.
2. `Dates needing review: ` followed by the number of dates that need review.

The expected output is:

~~~text
Changed dates: 2
Dates needing review: 1
~~~

Check compares your output with that, and ignores line endings and trailing spaces.

The ambiguous date is the one to think about. `03/04/2021` could be the third of April or the fourth of March, and no rule in the list lets a program choose. Leave it for review, and do not convert it. The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
