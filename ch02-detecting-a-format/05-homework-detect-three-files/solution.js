import { readFileSync } from "node:fs";
import path from "node:path";

const names = ["customers.parquet", "customers.xlsx", "customers-as-json.csv"];

// Checks the signatures in order, and returns the first kind that matches.
function kindOf(data) {
  const starts = (text) => data.subarray(0, text.length).equals(Buffer.from(text, "latin1"));
  if (starts("PAR1")) return "parquet";
  if (starts("PK\x03\x04")) return "zip";
  if (starts("\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1")) return "ole2";
  const first = data.toString("latin1").replace(/^[ \t\r\n]+/, "")[0];
  if (first === "[" || first === "{") return "json";
  if (starts("<?xml")) return "xml";
  if (data.includes(0)) return "binary";
  return "text";
}

for (const name of names) {
  const data = readFileSync(path.join(process.env.TRAINING_DATA, name));
  console.log(`${name}: ${kindOf(data)}`);
}
