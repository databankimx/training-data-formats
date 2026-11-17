import { readFileSync } from "node:fs";
import path from "node:path";

const data = readFileSync(path.join(process.env.TRAINING_DATA, "customers-windows-1252.csv"));
// Decode with the encoding the file was written in. The letter is given as an escape, so the source is plain ASCII.
const text = new TextDecoder("windows-1252").decode(data);
const count = text.split("\n").filter((line) => line.includes("\u00e9")).length;
console.log(`Lines containing e-acute: ${count}`);
