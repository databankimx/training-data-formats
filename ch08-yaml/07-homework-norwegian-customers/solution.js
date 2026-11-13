import { readFileSync } from "node:fs";
import path from "node:path";
import { load } from "js-yaml";

const customers = load(readFileSync(path.join(process.env.TRAINING_DATA, "customers.yaml"), "utf8"));
// The code is quoted in the file, so it arrives as text and compares as text.
const norwegian = customers.filter((customer) => customer.country_code === "NO").length;
console.log(`Norwegian customers: ${norwegian}`);
