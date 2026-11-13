import { createReadStream } from "node:fs";
import path from "node:path";
import readline from "node:readline";

const input = createReadStream(path.join(process.env.TRAINING_DATA, "orders-lines.jsonl"), { encoding: "utf8" });
const reader = readline.createInterface({ input, crlfDelay: Infinity });
let shipped = 0;
let skipped = 0;
for await (const line of reader) {
  let order;
  try {
    order = JSON.parse(line);
  } catch (error) {
    skipped++;
    continue;
  }
  if (order.status === "shipped") shipped++;
}
console.log(`Shipped orders: ${shipped}`);
console.log(`Skipped lines: ${skipped}`);
