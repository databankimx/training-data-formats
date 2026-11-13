import { readFileSync } from "node:fs";
import path from "node:path";
import { XMLParser } from "fast-xml-parser";

const parser = new XMLParser({ ignoreAttributes: false, attributeNamePrefix: "@_", processEntities: false, parseTagValue: false });
const orders = parser.parse(readFileSync(path.join(process.env.TRAINING_DATA, "orders.xml"), "utf8")).orders.order;
// The identifier is an attribute, so it is read with the @_ prefix.
const pending = orders.filter((order) => order.status === "pending").map((order) => order["@_id"]);
console.log(`Pending orders: ${pending.length}`);
console.log(`Pending ids: ${pending.join(", ")}`);
