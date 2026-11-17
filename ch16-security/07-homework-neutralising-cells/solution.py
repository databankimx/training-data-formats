# Inline data, not from a sample file. Four cell values, typed into the code, from a file someone else sent.
values = ["=1+1", "Alice", "-45.00", "@SUM(A1)"]
formula_starts = "=+-@"


def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


neutralised = 0
left_alone = 0
for value in values:
    if value and value[0] in formula_starts and not is_number(value):
        neutralised += 1
    else:
        left_alone += 1
print(f"Neutralised: {neutralised}")
print(f"Left alone: {left_alone}")
