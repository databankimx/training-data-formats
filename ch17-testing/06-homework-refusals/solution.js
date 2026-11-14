// Inline data, not from a sample file. Four inputs, typed into the code, sent to a JSON reader.
const inputs = ['[{"a":1}]', '[{"a":', "", '{"a":1}'];
let refused = 0;
let accepted = 0;
for (const text of inputs) {
  try {
    JSON.parse(text);
    accepted++;
  } catch (error) {
    if (error instanceof SyntaxError) refused++;
    else throw error;
  }
}
console.log(`Refused: ${refused}`);
console.log(`Accepted: ${accepted}`);
