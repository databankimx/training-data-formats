import { readFileSync } from "node:fs";
import path from "node:path";
import { XMLParser } from "fast-xml-parser";

// Entity processing is off, and tag values are kept as text, so each amount is read exactly as written.
const parser = new XMLParser({ processEntities: false, parseTagValue: false });
const orders = parser.parse(readFileSync(path.join(process.env.TRAINING_DATA, "orders.xml"), "utf8")).orders.order;
let shipped = 0;
// The amounts are summed in whole cents, so no binary float error builds up. The division happens once, at the end.
let cents = 0;
for (const order of orders) {
  if (order.status === "shipped") {
    shipped++;
    cents += Math.round(Number(order.amount) * 100);
  }
}
console.log(`Shipped orders: ${shipped}`);
console.log(`Shipped total: ${(cents / 100).toFixed(2)}`);
