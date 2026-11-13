import { readFileSync } from "node:fs";
import path from "node:path";

const data = readFileSync(path.join(process.env.TRAINING_DATA, "customers-utf8-bom.csv"));
// The mark is the three bytes EF BB BF. Check the bytes first, then decode without the mark.
const hasMark = data[0] === 0xef && data[1] === 0xbb && data[2] === 0xbf;
const text = data.subarray(hasMark ? 3 : 0).toString("utf8");
const header = text.split("\n")[0].split(",")[0];
console.log(`Starts with a byte-order mark: ${hasMark ? "yes" : "no"}`);
console.log(`First header: ${header}`);
