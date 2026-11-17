# Homework: Counting Unknown Fields

The three records below are typed into the code, so the data is inline. The record type you are given declares only `customer_id` and `name`, so every other field is unknown to it.

~~~text
[
  {"customer_id": 1, "name": "Ana Silva", "loyalty_points": 5},
  {"customer_id": 2, "name": "Ben Osei", "referrer": "1", "tier": "gold"},
  {"customer_id": 3, "name": "Cara Dunn"}
]
~~~

Read each record, and count every field that is not `customer_id` or `name`. Print two lines and nothing else:

1. `Records: ` followed by the number of records.
2. `Unknown fields: ` followed by the total number of unknown fields across all the records.

The expected output is:

~~~text
Records: 3
Unknown fields: 3
~~~

Check compares your output with that, and ignores line endings and trailing spaces.

Count every unknown field, not every record that has one. The second record has two unknown fields, so it adds two to the total. A record with no unknown fields adds nothing. Do not print the field names, since the expected output is the count alone. The starter files give you the first line of each program, and you write the rest. Press Show solution (spoiler) only after you've tried it.

---
