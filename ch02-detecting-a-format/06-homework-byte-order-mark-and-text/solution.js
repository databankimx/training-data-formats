import { readFileSync } from "node:fs";
import path from "node:path";

const names = ["customers-utf8-bom.csv", "customers-windows-1252.csv", "config-norway.yaml"];

for (const name of names) {
  const data = readFileSync(path.join(process.env.TRAINING_DATA, name));
  // The mark is checked on the bytes, before anything is decoded.
  const hasMark = data[0] === 0xef && data[1] === 0xbb && data[2] === 0xbf;
  // A file with no NUL byte is text. The mark doesn't change that.
  const kind = data.includes(0) ? "binary" : "text";
  const suffix = hasMark ? ", with byte-order mark" : "";
  console.log(`${name}: ${kind}${suffix}`);
}
