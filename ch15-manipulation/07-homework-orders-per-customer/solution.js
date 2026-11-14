import { readFileSync } from "node:fs";
import path from "node:path";
import { parse } from "csv-parse/sync";

const orders = parse(readFileSync(path.join(process.env.TRAINING_DATA, "orders.csv"), "utf8"), { columns: true });
const sizes = new Map();
for (const order of orders) {
  sizes.set(order.customer_id, (sizes.get(order.customer_id) ?? 0) + 1);
}
const counts = [...sizes.values()];
console.log(`Customers with more than one order: ${counts.filter((size) => size > 1).length}`);
console.log(`Most orders by one customer: ${Math.max(...counts)}`);
