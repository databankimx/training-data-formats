import os

from lxml import etree

path = os.path.join(os.environ["TRAINING_DATA"], "orders.xml")
parser = etree.XMLParser(resolve_entities=False, no_network=True)
root = etree.parse(path, parser).getroot()
# The identifier is an attribute, so it is read with get, not findtext.
pending = [order.get("id") for order in root.findall("order") if order.findtext("status") == "pending"]
print(f"Pending orders: {len(pending)}")
print(f"Pending ids: {', '.join(pending)}")
