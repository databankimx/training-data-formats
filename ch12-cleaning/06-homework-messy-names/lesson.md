# Homework: Messy Names and Codes

The three records below are typed into the code, so the data is inline. Each record has a name, a country code, and an email. Apply these rules to every value, and print two counts.

1. A name is trimmed, and each run of whitespace inside it becomes one space. A non-breaking space counts as whitespace.
2. A country code is made uppercase and trimmed.
3. An email that is empty needs review, and the cleaner does not change it.

The records are:

- `"  Alice   Carter "`, `"us"`, `"alice@example.invalid"`
- `"Chidi Okafor"`, `"GB"`, `""`
- `"Mei\u00A0Lin"`, `"SG"`, `"mei@example.invalid"`

Print two lines and nothing else:

1. `Changed values: ` followed by the number of name and country values that the rules changed.
2. `Values needing review: ` followed by the number of emails that need review.

The expected output is:

~~~text
Changed values: 3
Values needing review: 1
~~~

Check compares your output with that, and ignores line endings and trailing spaces.

Count each value, not each record. The first record contributes two changes, its name and its country code, and the third contributes one, its name. An unchanged value counts for nothing. The empty email is the only review item. The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
