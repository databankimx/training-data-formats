import { readFileSync } from "node:fs";
import path from "node:path";
import { parse } from "csv-parse/sync";

const rows = parse(readFileSync(path.join(process.env.TRAINING_DATA, "customers.csv"), "utf8")).slice(1);
// Column 5 is active, and column 10 is tags.
const active = rows.filter((row) => row[5] === "true").length;
const tagged = rows.filter((row) => row[10] !== "").length;
console.log(`Active customers: ${active}`);
console.log(`Tagged customers: ${tagged}`);
