import { readFileSync } from "node:fs";
import path from "node:path";

const data = readFileSync(path.join(process.env.TRAINING_DATA, "customers-mixed-line-endings.csv"));
// Every LF is one line. A CRLF is an LF with a carriage return before it.
let lines = 0;
let crlf = 0;
for (let i = 0; i < data.length; i++) {
  if (data[i] === 0x0a) {
    lines++;
    if (i > 0 && data[i - 1] === 0x0d) crlf++;
  }
}
console.log(`Lines: ${lines}`);
console.log(`CRLF: ${crlf}`);
console.log(`LF only: ${lines - crlf}`);
