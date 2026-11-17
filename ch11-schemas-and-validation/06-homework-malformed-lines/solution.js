import { readFileSync } from "node:fs";
import path from "node:path";

// Inline data, not from a sample file. The statuses an order may have.
const allowed = new Set(["pending", "paid", "shipped", "refunded"]);
const lines = readFileSync(path.join(process.env.TRAINING_DATA, "orders-lines.jsonl"), "utf8").split("\n").filter((line) => line !== "");
let failing = 0;
lines.forEach((line, index) => {
  let order;
  try {
    order = JSON.parse(line);
  } catch (error) {
    console.log(`Line ${index + 1}: not valid JSON`);
    failing++;
    return;
  }
  if (!allowed.has(order.status)) {
    console.log(`Line ${index + 1}: status is not allowed`);
    failing++;
  }
});
console.log(`Lines checked: ${lines.length}`);
console.log(`Lines failing: ${failing}`);
