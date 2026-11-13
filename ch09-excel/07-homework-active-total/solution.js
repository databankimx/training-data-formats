import { readFileSync } from "node:fs";
import path from "node:path";
import ExcelJS from "exceljs";

const workbook = new ExcelJS.Workbook();
await workbook.xlsx.readFile(path.join(process.env.TRAINING_DATA, "customers.xlsx"));
const rows = [];
workbook.getWorksheet("customers").eachRow((row, rowNumber) => {
  if (rowNumber > 1) rows.push(row);
});
// Column 6 is active, and column 5 is balance. The balances are summed in whole cents, so no binary float error builds up.
const active = rows.filter((row) => row.getCell(6).value === true).length;
const cents = rows.reduce((sum, row) => sum + Math.round(row.getCell(5).value * 100), 0);
console.log(`Active customers: ${active}`);
console.log(`Total balance: ${(cents / 100).toFixed(2)}`);
