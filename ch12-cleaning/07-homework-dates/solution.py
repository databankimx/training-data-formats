import re
from datetime import datetime

# Inline data, not from a sample file. Four dates in mixed forms.
dates = ["03/04/2021", "14/03/2021", "2021-3-4", "2021-03-04"]


def is_real_date(text):
    try:
        datetime.strptime(text, "%Y-%m-%d")
    except ValueError:
        return False
    return True


changed = 0
review = 0
for date in dates:
    iso = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", date)
    slash = re.fullmatch(r"(\d{2})/(\d{2})/(\d{4})", date)
    if iso and len(iso.group(2)) == 2 and len(iso.group(3)) == 2:
        # Already in the ISO form. It is unchanged when it is a real date, and otherwise it needs review.
        if not is_real_date(date):
            review += 1
        continue
    if slash:
        if int(slash.group(1)) > 12:
            changed += 1
        else:
            review += 1
        continue
    if iso:
        padded = f"{iso.group(1)}-{int(iso.group(2)):02d}-{int(iso.group(3)):02d}"
        if is_real_date(padded):
            changed += 1
        else:
            review += 1
print(f"Changed dates: {changed}")
print(f"Dates needing review: {review}")
