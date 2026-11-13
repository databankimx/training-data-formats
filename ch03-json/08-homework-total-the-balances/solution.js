import { readFileSync } from "node:fs";
import path from "node:path";

const customers = JSON.parse(readFileSync(path.join(process.env.TRAINING_DATA, "customers.json"), "utf8"));
const active = customers.filter((customer) => customer.active).length;
// Balances are summed in whole cents, so no binary float error builds up. The division happens once, at the end.
const cents = customers.reduce((sum, customer) => sum + Math.round(customer.balance * 100), 0);
console.log(`Active customers: ${active}`);
console.log(`Total balance: ${(cents / 100).toFixed(2)}`);
