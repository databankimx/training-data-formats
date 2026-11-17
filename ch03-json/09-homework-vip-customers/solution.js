import { readFileSync } from "node:fs";
import path from "node:path";

const customers = JSON.parse(readFileSync(path.join(process.env.TRAINING_DATA, "customers.json"), "utf8"));
for (const customer of customers) {
  // includes checks the list for the exact tag, so a customer with no vip tag is skipped.
  if (customer.tags.includes("vip")) {
    console.log(`${customer.customer_id} ${customer.address.city}`);
  }
}
