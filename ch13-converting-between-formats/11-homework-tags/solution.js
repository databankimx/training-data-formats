import { readFileSync } from "node:fs";
import path from "node:path";
import { parse } from "csv-parse/sync";

const rows = parse(readFileSync(path.join(process.env.TRAINING_DATA, "customers.csv"), "utf8"), { columns: true });
let total = 0;
let empty = 0;
for (const row of rows) {
  // Empty items are dropped, so a customer with no tags has an empty list, not a list with one empty item.
  const tags = row.tags.split(";").filter((tag) => tag !== "");
  total += tags.length;
  if (tags.length === 0) empty++;
}
console.log(`Tags in the list: ${total}`);
console.log(`Customers with no tags: ${empty}`);
