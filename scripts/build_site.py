
from pathlib import Path
from html import escape
import shutil
import re

ROOT = Path(__file__).resolve().parent.parent
MEMBERS = ROOT / "members"
OUTPUT = ROOT / "_site"

# Διαβάζουμε την κεντρική σελίδα
index_file = ROOT / "index.html"
html = index_file.read_text(encoding="utf-8")

# Βρίσκουμε τα βιογραφικά των μελών
cv_files = sorted(MEMBERS.glob("*.html"))


def prettify_name(filename_stem):
    name = re.sub(r"([a-z])([A-Z])", r"\1 \2", filename_stem)
    return name.replace("_", " ").replace("-", " ").strip()


def initials_for(name):
    parts = name.split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[1][0]).upper()
    return name[:2].upper() if name else "CV"


# Δημιουργούμε τις κάρτες της κεντρικής σελίδας
cards = []

for cv in cv_files:
    name = prettify_name(cv.stem)
    initials = initials_for(name)

    cards.append(f'''
<article class="card">
  <div class="avatar">{escape(initials)}</div>
  <h2>{escape(name)}</h2>
  <p>Μέλος της ομάδας</p>
  <a class="btn"
     href="members/{escape(cv.name, quote=True)}"
     target="_blank"
     rel="noopener noreferrer">
     Δες το βιογραφικό →
  </a>
</article>'''.strip())

# Αντικατάσταση του CV_LINKS
if "<!-- CV_LINKS -->" not in html:
    raise ValueError(
        "Δεν βρέθηκε το σημείο <!-- CV_LINKS --> στο index.html"
    )

html = html.replace("<!-- CV_LINKS -->", "\n".join(cards))

# Δημιουργούμε τον φάκελο της δημοσιευμένης ιστοσελίδας
if OUTPUT.exists():
    shutil.rmtree(OUTPUT)

OUTPUT.mkdir(parents=True)

(OUTPUT / "index.html").write_text(
    html, encoding="utf-8"
)

# Αντιγράφουμε όλα τα αρχεία των μελών
output_members = OUTPUT / "members"
shutil.copytree(MEMBERS, output_members)

# Δημιουργούμε το Webring σε κάθε δημοσιευμένο βιογραφικό
for i, cv in enumerate(cv_files):

    previous_cv = cv_files[(i - 1) % len(cv_files)]
    next_cv = cv_files[(i + 1) % len(cv_files)]

    page = output_members / cv.name
    cv_html = page.read_text(encoding="utf-8")

    navigation = f'''
<nav class="sdy60-webring"
     aria-label="Πλοήγηση στα βιογραφικά της ομάδας">

  <a href="{escape(previous_cv.name, quote=True)}">
    ← Προηγούμενο
  </a>

  <a href="../index.html">
    Ομάδα ΣΔΥ60
  </a>

  <a href="{escape(next_cv.name, quote=True)}">
    Επόμενο →
  </a>

</nav>

<style>
  .sdy60-webring {{
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 12px;
    margin: 28px auto;
    padding: 12px;
    font-family: 'Segoe UI', Arial, sans-serif;
  }}

  .sdy60-webring a {{
    display: inline-block;
    padding: 10px 15px;
    border-radius: 10px;
    background: #7568d8;
    color: white;
    text-decoration: none;
  }}

  .sdy60-webring a:hover {{
    background: #2800a8;
  }}
</style>
'''

    # Προσθέτουμε το Webring πριν από το κλείσιμο του body
    if re.search(r"</body\s*>", cv_html, flags=re.IGNORECASE):
        cv_html = re.sub(
            r"</body\s*>",
            lambda match: navigation + "\n" + match.group(0),
            cv_html,
            count=1,
            flags=re.IGNORECASE
        )
    else:
        cv_html += navigation

    page.write_text(cv_html, encoding="utf-8")

print(
    f"Η ιστοσελίδα δημιουργήθηκε με "
    f"{len(cv_files)} βιογραφικά και Webring."
)
