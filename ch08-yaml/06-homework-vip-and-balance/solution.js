import { readFileSync } from "node:fs";
import path from "node:path";
import { load } from "js-yaml";

const customers = load(readFileSync(path.join(process.env.TRAINING_DATA, "customers.yaml"), "utf8"));
const vip = customers.filter((customer) => customer.tags.includes("vip")).length;
// The balances are summed in whole cents, so no binary float error builds up. The division happens once, at the end.
const cents = customers.reduce((sum, customer) => sum + Math.round(Number(customer.balance) * 100), 0);
console.log(`VIP customers: ${vip}`);
console.log(`Total balance: ${(cents / 100).toFixed(2)}`);
