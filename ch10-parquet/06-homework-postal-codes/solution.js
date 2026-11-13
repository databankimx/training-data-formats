import path from "node:path";
import { asyncBufferFromFile, parquetReadObjects } from "hyparquet";

const rows = await parquetReadObjects({ file: await asyncBufferFromFile(path.join(process.env.TRAINING_DATA, "customers.parquet")) });
// The postal code is a string, so its leading zeros are kept, and the first character is tested.
const zeroStart = rows.filter((row) => String(row.address.postal_code).startsWith("0")).length;
console.log(`Postal codes starting with 0: ${zeroStart}`);
