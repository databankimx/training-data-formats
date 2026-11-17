import { readFileSync } from "node:fs";
import path from "node:path";

const lines = readFileSync(path.join(process.env.TRAINING_DATA, "customers.fixed"), "utf8").split("\n").filter((line) => line !== "");
let active = 0;
let largest = -Infinity;
let largestText = "";
for (const line of lines) {
  // The active flag is at positions 49 to 53, and the balance at positions 40 to 47.
  if (line.slice(48, 53).trim() === "true") active++;
  const text = line.slice(39, 47).trim();
  const value = Number(text);
  if (value > largest) {
    largest = value;
    largestText = text;
  }
}
console.log(`Active customers: ${active}`);
console.log(`Largest balance: ${largestText}`);
