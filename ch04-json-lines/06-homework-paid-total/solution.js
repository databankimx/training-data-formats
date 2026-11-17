import { createReadStream } from "node:fs";
import path from "node:path";
import readline from "node:readline";

const input = createReadStream(path.join(process.env.TRAINING_DATA, "orders-lines.jsonl"), { encoding: "utf8" });
const reader = readline.createInterface({ input, crlfDelay: Infinity });
let paidCount = 0;
let cents = 0;
for await (const line of reader) {
  let order;
  try {
    order = JSON.parse(line);
  } catch (error) {
    continue;
  }
  if (order.status === "paid") {
    paidCount++;
    // The amount is text. Convert it to whole cents, so the sum stays exact.
    cents += Math.round(Number(order.amount) * 100);
  }
}
console.log(`Paid orders: ${paidCount}`);
console.log(`Paid total: ${(cents / 100).toFixed(2)}`);
