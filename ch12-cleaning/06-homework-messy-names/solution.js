// Inline data, not from a sample file. Name, country code, and email for three customers.
const records = [
  ["  Alice   Carter ", "us", "alice@example.invalid"],
  ["Chidi Okafor", "GB", ""],
  ["Mei\u00a0Lin", "SG", "mei@example.invalid"],
];
let changed = 0;
let review = 0;
for (const [name, country, email] of records) {
  const cleanedName = name.replace(/\s+/g, " ").trim();
  if (cleanedName !== name) changed++;
  const cleanedCountry = country.trim().toUpperCase();
  if (cleanedCountry !== country) changed++;
  if (email === "") review++;
}
console.log(`Changed values: ${changed}`);
console.log(`Values needing review: ${review}`);
