// Converts a balance's text to whole cents, splitting at the decimal point so no binary float is used.
function toCents(text) {
  const [pounds, cents = ""] = text.split(".");
  return Number(pounds) * 100 + (cents === "" ? 0 : Number(cents.padEnd(2, "0")));
}

// Inline data, not from a sample file. Four cases, typed into the code, with the expected cents.
const cases = [["1250.75", 125075], ["0.00", 0], ["980.1", 98010], ["4410", 441000]];
let passed = 0;
let failed = 0;
for (const [text, expected] of cases) {
  if (toCents(text) === expected) passed++;
  else failed++;
}
console.log(`Cases passed: ${passed}`);
console.log(`Cases failed: ${failed}`);
