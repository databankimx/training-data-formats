import { readFileSync } from "node:fs";
import path from "node:path";
import { parse } from "csv-parse/sync";

const records = parse(readFileSync(path.join(process.env.TRAINING_DATA, "customers-duplicates.csv"), "utf8")).slice(1);
const seen = new Set();
const repeated = [];
for (const record of records) {
  const id = record[0];
  if (seen.has(id) && !repeated.includes(id)) repeated.push(id);
  seen.add(id);
}
console.log(`Rows: ${records.length}`);
console.log(`Unique customer ids: ${seen.size}`);
console.log(`Repeated ids: ${repeated.join(", ")}`);
