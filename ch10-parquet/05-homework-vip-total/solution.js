import path from "node:path";
import { asyncBufferFromFile, parquetReadObjects } from "hyparquet";

const rows = await parquetReadObjects({ file: await asyncBufferFromFile(path.join(process.env.TRAINING_DATA, "customers.parquet")) });
const vip = rows.filter((row) => row.tags.includes("vip")).length;
// hyparquet returns a decimal as a number, so the balances are summed in whole cents to avoid binary float drift.
const cents = rows.reduce((sum, row) => sum + Math.round(Number(row.balance) * 100), 0);
console.log(`VIP customers: ${vip}`);
console.log(`Total balance: ${(cents / 100).toFixed(2)}`);
