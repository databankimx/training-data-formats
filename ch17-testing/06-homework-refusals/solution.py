# Inline data, not from a sample file. Four inputs, typed into the code, sent to a JSON reader.
import json

inputs = ['[{"a":1}]', '[{"a":', "", '{"a":1}']
refused = 0
accepted = 0
for text in inputs:
    try:
        json.loads(text)
        accepted += 1
    except json.JSONDecodeError:
        refused += 1
print(f"Refused: {refused}")
print(f"Accepted: {accepted}")
