import os
from decimal import Decimal

from lxml import etree

path = os.path.join(os.environ["TRAINING_DATA"], "orders.xml")
parser = etree.XMLParser(resolve_entities=False, no_network=True)
root = etree.parse(path, parser).getroot()
shipped = 0
# Decimal keeps each amount exact, so the total has no floating-point drift.
total = Decimal("0")
for order in root.findall("order"):
    if order.findtext("status") == "shipped":
        shipped += 1
        total += Decimal(order.findtext("amount"))
print(f"Shipped orders: {shipped}")
print(f"Shipped total: {total:.2f}")
