// Inline data, not from a sample file. Four dates in mixed forms.
const dates = ["03/04/2021", "14/03/2021", "2021-3-4", "2021-03-04"];

// True when the text is a real date in the ISO form.
function isRealDate(text) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(text)) return false;
  const [year, month, day] = text.split("-").map(Number);
  const date = new Date(Date.UTC(year, month - 1, day));
  return date.getUTCMonth() === month - 1 && date.getUTCDate() === day;
}

let changed = 0;
let review = 0;
for (const date of dates) {
  const iso = date.match(/^(\d{4})-(\d{1,2})-(\d{1,2})$/);
  const slash = date.match(/^(\d{2})\/(\d{2})\/(\d{4})$/);
  if (iso && iso[2].length === 2 && iso[3].length === 2) {
    // Already in the ISO form. It is unchanged when it is a real date, and otherwise it needs review.
    if (!isRealDate(date)) review++;
    continue;
  }
  if (slash) {
    if (Number(slash[1]) > 12) {
      changed++;
    } else {
      review++;
    }
    continue;
  }
  if (iso) {
    const padded = `${iso[1]}-${iso[2].padStart(2, "0")}-${iso[3].padStart(2, "0")}`;
    if (isRealDate(padded)) {
      changed++;
    } else {
      review++;
    }
  }
}
console.log(`Changed dates: ${changed}`);
console.log(`Dates needing review: ${review}`);
