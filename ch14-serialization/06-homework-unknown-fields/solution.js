// Inline data, not from a sample file. Three records, typed into the code, with fields the record type does not declare.
const text = '[{"customer_id":1,"name":"Ana Silva","loyalty_points":5},{"customer_id":2,"name":"Ben Osei","referrer":"1","tier":"gold"},{"customer_id":3,"name":"Cara Dunn"}]';
const known = new Set(["customer_id", "name"]);
const records = JSON.parse(text);
const unknown = records.reduce((sum, record) => sum + Object.keys(record).filter((name) => !known.has(name)).length, 0);
console.log(`Records: ${records.length}`);
console.log(`Unknown fields: ${unknown}`);
