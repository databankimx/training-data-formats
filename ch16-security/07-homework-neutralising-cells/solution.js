// Inline data, not from a sample file. Four cell values, typed into the code, from a file someone else sent.
const values = ["=1+1", "Alice", "-45.00", "@SUM(A1)"];
const formulaStarts = ["=", "+", "-", "@"];
let neutralised = 0;
let leftAlone = 0;
for (const value of values) {
  const isNumber = value.trim() !== "" && !Number.isNaN(Number(value));
  if (value.length > 0 && formulaStarts.includes(value[0]) && !isNumber) {
    neutralised++;
  } else {
    leftAlone++;
  }
}
console.log(`Neutralised: ${neutralised}`);
console.log(`Left alone: ${leftAlone}`);
