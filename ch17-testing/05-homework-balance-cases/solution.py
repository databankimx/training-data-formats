def to_cents(text):
    # Splits at the decimal point, so no binary float is used.
    pounds, _, cents = text.partition(".")
    return int(pounds) * 100 + (int(cents.ljust(2, "0")) if cents else 0)


# Inline data, not from a sample file. Four cases, typed into the code, with the expected cents.
cases = [("1250.75", 125075), ("0.00", 0), ("980.1", 98010), ("4410", 441000)]
passed = 0
failed = 0
for text, expected in cases:
    if to_cents(text) == expected:
        passed += 1
    else:
        failed += 1
print(f"Cases passed: {passed}")
print(f"Cases failed: {failed}")
