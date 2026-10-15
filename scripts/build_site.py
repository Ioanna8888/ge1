from pathlib import Path
from html import escape
import shutil

ROOT = Path(__file__).resolve().parent.parent
MEMBERS = ROOT / "members"
OUTPUT = ROOT / "_site"

# Διαβάζουμε την κεντρική σελίδα
index_file = ROOT / "index.html"
html = index_file.read_text(encoding="utf-8")

# Βρίσκουμε τα βιογραφικά των μελών
cv_files = sorted(MEMBERS.glob("*.html"))

links = []
for cv in cv_files:
    name = cv.stem.replace("_", " ").replace("-", " ")
    links.append(
        f'<li><a href="members/{escape(cv.name, quote=True)}">'
        f'{escape(name)}</a></li>'
    )

cv_list = "<ul>\n" + "\n".join(links) + "\n</ul>"

# Αντικαθιστούμε το ειδικό σημείο της αρχικής σελίδας
if "<!-- CV_LINKS -->" not in html:
    raise ValueError("Δεν βρέθηκε το σημείο CV_LINKS στο index.html")

html = html.replace("<!-- CV_LINKS -->", cv_list)

# Δημιουργούμε τον φάκελο της δημοσιευμένης ιστοσελίδας
if OUTPUT.exists():
    shutil.rmtree(OUTPUT)

OUTPUT.mkdir()
(OUTPUT / "index.html").write_text(html, encoding="utf-8")

# Αντιγράφουμε τα βιογραφικά στη δημοσιευμένη ιστοσελίδα
output_members = OUTPUT / "members"
output_members.mkdir()

for cv in cv_files:
    shutil.copy2(cv, output_members / cv.name)

print(f"Η ιστοσελίδα δημιουργήθηκε με {len(cv_files)} βιογραφικά.")
