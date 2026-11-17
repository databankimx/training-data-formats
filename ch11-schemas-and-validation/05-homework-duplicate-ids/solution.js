import { readFileSync } from "node:fs";
import path from "node:path";
import { parse } from "csv-parse/sync";

const body = parse(readFileSync(path.join(process.env.TRAINING_DATA, "customers-duplicates.csv"), "utf8")).slice(1);
const seen = new Set();
let failing = 0;
body.forEach((row, index) => {
  const id = row[0];
  // A row fails when its identifier has already appeared on an earlier row.
  if (seen.has(id)) {
    console.log(`Line ${index + 2}: customer_id ${id} is a duplicate`);
    failing++;
  }
  seen.add(id);
});
console.log(`Rows checked: ${body.length}`);
console.log(`Rows failing: ${failing}`);
