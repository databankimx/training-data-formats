# What a Schema Is

A schema is a list of rules, one set for each column. Each rule says what a value must be, and whether it may be missing. For the customer data, the schema in this chapter has eight columns:

| Column | Rule |
|---|---|
| `customer_id` | Required. A whole number, and unique within the file. |
| `name` | Required. Text, and not empty. |
| `email` | Required. Text. |
| `signup_date` | Required. A date in `YYYY-MM-DD` form that exists on the calendar. |
| `balance` | Required. A decimal with exactly two places. |
| `active` | Required. `true` or `false`. |
| `country_code` | Required. Two uppercase letters. |
| `tags` | Required, and may be an empty list. It may not be null. |

The rules are about the data, not the format. The same schema applies to a CSV file, where every value is text and the checks parse it, and to a JSON file, where a number is already a number and a missing value can be null or absent. The check must be written for each format's representation, but the rules stay the same.

A validator checks each row against each rule, and it reports every failure it finds, with the location of the row. Stopping at the first failure hides the rest, and a file with twelve bad rows would need twelve runs to find them. Reporting the location matters as much: a person who receives a message such as "signup_date is not valid" needs to know which line to fix.

Two rules deserve care. A rule for a date must check the calendar as well as the shape. `2021-02-30` has the right form, with four digits, a dash, two digits, a dash, and two digits, but February has no thirtieth day, so the value is not a date. A pattern check alone would accept it. The rule for a missing value must also distinguish null from absent: a required field that is null fails, and a required field that is absent fails too, but the message should say which, because the fix is different.

> **Aside: the schema is a document, not a class.**
> A schema written as rules can be read by a person, checked against a file, and kept with the data. A class in code can do the same job for one program, but it doesn't travel with the file, and a second program that reads the file has to write its own copy.

> **Common mistake.** Writing a validator that checks only the rules a file is known to fail. The check passes for every file that has the one bad value it was written for, and it misses everything else. Check every rule on every row.

---
