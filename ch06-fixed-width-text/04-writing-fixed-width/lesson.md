# Writing Fixed-Width Text

Writing fixed-width text is the reverse of reading. Each value is padded to its column's width, with the padding on the side the alignment sets. A number is padded on the left, so its digits line up at the right edge. A name is padded on the right, so its first letter lines up at the left edge. Then the columns are joined, with the gaps the layout leaves between them.

The sample below writes three customers from the code, using the same layout as before. The customers are typed into the code, so the data is inline. Each language has a padding function, and the output is the same in each.

~~~examples
```csharp
// The two lines below suppress compiler warnings that would confuse a learner. They are not part of the exercise.
#:property Nullable=disable
#:property PublishAot=false

// Inline data, not from a sample file. Three customers, typed into the code, to be written at fixed positions.
var customers = new[]
{
    ("1001", "Alice Carter", "1250.75"),
    ("1002", "Chidi Okafor", "0.00"),
    ("1003", "Mei Lin", "75.50"),
};
foreach (var (id, name, balance) in customers)
{
    // The identifier is right-aligned in 6 columns, the name left-aligned in 20, and the balance right-aligned in 8.
    var line = id.PadLeft(6) + " " + name.PadRight(20) + " " + balance.PadLeft(8);
    Console.WriteLine(line);
}
```
```python
# Inline data, not from a sample file. Three customers, typed into the code, to be written at fixed positions.
customers = [
    ("1001", "Alice Carter", "1250.75"),
    ("1002", "Chidi Okafor", "0.00"),
    ("1003", "Mei Lin", "75.50"),
]
for customer_id, name, balance in customers:
    # The identifier is right-aligned in 6 columns, the name left-aligned in 20, and the balance right-aligned in 8.
    print(f"{customer_id:>6} {name:<20} {balance:>8}")
```
```javascript
// Inline data, not from a sample file. Three customers, typed into the code, to be written at fixed positions.
const customers = [
  ["1001", "Alice Carter", "1250.75"],
  ["1002", "Chidi Okafor", "0.00"],
  ["1003", "Mei Lin", "75.50"],
];
for (const [customerId, name, balance] of customers) {
  // The identifier is right-aligned in 6 columns, the name left-aligned in 20, and the balance right-aligned in 8.
  console.log(`${customerId.padStart(6)} ${name.padEnd(20)} ${balance.padStart(8)}`);
}
```
~~~

The output is the same in every language:

~~~text
  1001 Alice Carter          1250.75
  1002 Chidi Okafor             0.00
  1003 Mei Lin                 75.50
~~~

Count the spaces before each balance, and you'll see why the layout works. The balance ends at the same column in all three lines, even though the names have different lengths and the balances have different numbers of digits. The name is padded to 20 characters, so the gap after it is always the same, and the balance is padded to 8, so its digits end at position 36, the last column of this three-column line.

Writing is where width errors show up first. A value wider than its column has to be refused, or truncated on purpose, because the padding function will pass it through unchanged and the next column will move. The sample doesn't have such a value, so the padding never overflows. Add one, and the line lengthens and the balance moves.

> **Aside: pad, don't join.**
> A line built from a fixed set of padded values has the same length every time. A line built by joining strings with spaces does not, and a layout written that way is only correct for the values in the test.

> **Common mistake.** Padding a number on the right, because it looks tidier in a text editor. The reader cuts the balance from the right edge, so a right-padded number is cut in the wrong place, and the value is read as a different number.

---
