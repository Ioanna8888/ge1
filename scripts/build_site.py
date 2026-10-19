
# Γράφουμε το νέο index.html
(OUTPUT / "index.html").write_text(html, encoding="utf-8")

# Αντιγραφή φακέλου members με όλα τα αρχεία (html, jpg, png κτλ)
output_members = OUTPUT / "members"
shutil.copytree(MEMBERS, output_members)

# Webring: προσθέτουμε κυκλική πλοήγηση μόνο στα δημοσιευμένα βιογραφικά.
# Τα πρωτότυπα HTML του φακέλου members δεν τροποποιούνται.
for i, cv in enumerate(cv_files):
    previous_cv = cv_files[(i - 1) % len(cv_files)]
    next_cv = cv_files[(i + 1) % len(cv_files)]

    previous_url = escape(previous_cv.name, quote=True)
    next_url = escape(next_cv.name, quote=True)

    webring_html = f"""
<!-- SDY60 WEBRING -->
<nav aria-label="Πλοήγηση στα βιογραφικά της ομάδας ΣΔΥ60"
     style="display:flex;flex-wrap:wrap;justify-content:center;gap:12px;
            margin:30px auto;padding:16px;text-align:center;">
  <a href="{previous_url}" style="color:#594ac2;">← Προηγούμενο βιογραφικό</a>
  <a href="../index.html" style="color:#594ac2;">Ομάδα ΣΔΥ60</a>
  <a href="{next_url}" style="color:#594ac2;">Επόμενο βιογραφικό →</a>
</nav>
<!-- /SDY60 WEBRING -->
"""

    published_cv = output_members / cv.name
    cv_html = published_cv.read_text(encoding="utf-8")
    # Εισαγωγή πριν από το τέλος του body, ανεξάρτητα από πεζά/κεφαλαία.
    if re.search(r"</body\s*>", cv_html, flags=re.IGNORECASE):
        cv_html = re.sub(r"</body\s*>",
                         lambda match: webring_html + "\n" + match.group(0),
                         cv_html, count=1, flags=re.IGNORECASE)
    else:
        cv_html += webring_html
    published_cv.write_text(cv_html, encoding="utf-8")

print(f"Η ιστοσελίδα δημιουργήθηκε με {len(cv_files)} βιογραφικά σε μορφή καρτών και Webring.")
