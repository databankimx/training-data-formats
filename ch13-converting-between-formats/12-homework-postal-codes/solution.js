import { readFileSync } from "node:fs";
import path from "node:path";
import { parse } from "csv-parse/sync";

const rows = parse(readFileSync(path.join(process.env.TRAINING_DATA, "customers.csv"), "utf8"), { columns: true });
let changed = 0;
for (const row of rows) {
  const code = row.address_postal_code;
  // Only all-digit codes are numbers. Each is converted to a number and back, and compared as text.
  if (!/^\d+$/.test(code)) continue;
  if (String(Number(code)) !== code) changed++;
}
console.log(`Postal codes that change: ${changed}`);
