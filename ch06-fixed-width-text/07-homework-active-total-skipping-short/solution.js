import { readFileSync } from "node:fs";
import path from "node:path";

const lines = readFileSync(path.join(process.env.TRAINING_DATA, "customers-fixed-short-row.fixed"), "utf8").split("\n").filter((line) => line !== "");
const layoutLength = 56;
let counted = 0;
let skipped = 0;
// The balances are summed in whole cents, so no binary float error builds up. The division happens once, at the end.
let cents = 0;
for (const line of lines) {
  if (line.length < layoutLength) {
    skipped++;
    continue;
  }
  if (line.slice(48, 53).trim() === "true") {
    counted++;
    cents += Math.round(Number(line.slice(39, 47).trim()) * 100);
  }
}
console.log(`Active customers counted: ${counted}`);
console.log(`Active total: ${(cents / 100).toFixed(2)}`);
console.log(`Skipped short lines: ${skipped}`);
