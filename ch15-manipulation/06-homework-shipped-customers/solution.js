import { readFileSync } from "node:fs";
import path from "node:path";
import { parse } from "csv-parse/sync";

const orders = parse(readFileSync(path.join(process.env.TRAINING_DATA, "orders.csv"), "utf8"), { columns: true });
const shipped = orders.filter((order) => order.status === "shipped");
const customers = new Set(shipped.map((order) => order.customer_id));
// The amounts are summed in whole cents, so no binary float error builds up. The division happens once, at the end.
const cents = shipped.reduce((sum, order) => sum + Math.round(Number(order.amount) * 100), 0);
console.log(`Customers with a shipped order: ${customers.size}`);
console.log(`Shipped total: ${(cents / 100).toFixed(2)}`);
