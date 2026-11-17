import { createReadStream } from "node:fs";
import path from "node:path";
import readline from "node:readline";

const reader = readline.createInterface({
  input: createReadStream(path.join(process.env.TRAINING_DATA, "customers.csv"), { encoding: "utf8" }),
  crlfDelay: Infinity,
});
const limit = 10;
let accepted = 0;
let refused = 0;
let first = true;
for await (const line of reader) {
  // The header is not a data row, so it is skipped before the count begins.
  if (first) {
    first = false;
    continue;
  }
  if (accepted < limit) {
    accepted++;
  } else {
    refused++;
  }
}
console.log(`Rows accepted: ${accepted}`);
console.log(`Rows refused: ${refused}`);
