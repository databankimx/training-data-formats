import ExcelJS from "exceljs";
import path from "node:path";

const workbook = new ExcelJS.Workbook();
await workbook.xlsx.readFile(path.join(process.env.TRAINING_DATA, "customers-text-numbers.xlsx"));
const values = [];
workbook.getWorksheet("customers").eachRow((row, rowNumber) => {
  if (rowNumber > 1) values.push(row.getCell(5).value);
});
const textCount = values.filter((value) => typeof value === "string").length;
// Each text balance is converted to whole cents, so no binary float error builds up in the total.
const cents = values.reduce((sum, value) => sum + Math.round(Number(value) * 100), 0);
console.log(`Text balances: ${textCount}`);
console.log(`Text total: ${(cents / 100).toFixed(2)}`);
