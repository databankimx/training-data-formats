import json

# Inline data, not from a sample file. Three records, typed into the code, with fields the record type does not declare.
text = '[{"customer_id":1,"name":"Ana Silva","loyalty_points":5},{"customer_id":2,"name":"Ben Osei","referrer":"1","tier":"gold"},{"customer_id":3,"name":"Cara Dunn"}]'
known = {"customer_id", "name"}
records = json.loads(text)
unknown = sum(1 for record in records for name in record if name not in known)
print(f"Records: {len(records)}")
print(f"Unknown fields: {unknown}")
