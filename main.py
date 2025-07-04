import requests
import base64
import os
import random
import smtplib
from email.mime.text import MIMEText

# === CONFIG ===
wp_url = os.environ.get('WP_URL')
wp_user = os.environ.get('WP_USER')
wp_password = os.environ.get('WP_APP_PASSWORD')

notify_email = os.environ.get('EMAIL_NOTIFY')
email_user = os.environ.get('EMAIL_USER')
email_pass = os.environ.get('EMAIL_PASS')

# === TITELS ===
title_options = [
    "Zo verbeter je je online zichtbaarheid in Zuid-Holland",
    "Waarom SEO cruciaal is voor ondernemers in Zuid-Holland",
    "Een contentstrategie die werkt voor MKB in Zuid-Holland",
    "Lokale marketingtips voor bedrijven in Rotterdam & omgeving",
    "Meer leads en zichtbaarheid via SEO: zo pak je het aan"
]
title = random.choice(title_options)

# === AUTH ===
auth = base64.b64encode(f"{wp_user}:{wp_password}".encode()).decode("utf-8")
headers = {
    "Authorization": f"Basic {auth}",
    "Content-Type": "application/json"
}

# === INHOUD BLOG ===
intro = """
<p><strong>Als ondernemer in Zuid-Holland weet je hoe belangrijk het is om online gevonden te worden.</strong>
In deze blog leer je hoe je met slimme SEO en contentmarketing meer verkeer én klanten aantrekt.</p>
"""

h1 = "<h3>Wat is lokale SEO precies?</h3>"
p1 = "<p>Lokale SEO richt zich op het vindbaar maken van je bedrijf in je directe omgeving. Denk aan zoekopdrachten als 'marketingbureau Rotterdam' of 'webdesign Den Haag'. Door je website en content lokaal te optimaliseren, sta je sneller bovenaan in Google.</p>"

h2 = "<h3>Content die vertrouwen opbouwt</h3>"
p2 = "<p>Publiceer regelmatig waardevolle content die inspeelt op vragen van jouw doelgroep. Denk aan blogs, checklists of klantverhalen. Schrijf minimaal 600 woorden en gebruik relevante zoekwoorden zoals 'SEO Zuid-Holland'.</p>"

h3 = "<h3>Techniek en snelheid: de onzichtbare helden</h3>"
p3 = "<p>Een snelle, technisch goed gebouwde website is essentieel. Gebruik Google PageSpeed Insights en GTmetrix om optimalisaties te vinden.</p>"

h4 = "<h3>Gebruik Google Mijn Bedrijf</h3>"
p4 = "<p>Een goed Google Business-profiel maakt je zichtbaar in Google Maps en lokale zoekresultaten. Vraag reviews, upload foto’s en hou je info actueel.</p>"

outro = """
<p><strong>Klaar om hoger te ranken in Google?</strong>
FBN Marketing helpt bedrijven in Zuid-Holland groeien met SEO. Vraag nu een vrijblijvende scan aan van je website.</p>
"""

html_content = intro + h1 + p1 + h2 + p2 + h3 + p3 + h4 + p4 + outro

# === YOAST ===
seo_meta = {
    "yoast_title": title,
    "yoast_meta": f"{title} - SEO tips voor ondernemers in Zuid-Holland.",
    "yoast_focuskw": "SEO Zuid-Holland"
}

# === POST AANMAKEN ===
post_data = {
    "title": title,
    "status": "publish",
    "content": html_content,
    "meta": seo_meta
}

res = requests.post(f"{wp_url}/wp-json/wp/v2/posts", headers=headers, json=post_data)

if res.status_code == 201:
    post = res.json()
    link = post['link']
    print("✅ Blog geplaatst:", link)

    # === EMAIL STUREN ===
    msg = MIMEText(f"Nieuwe blog geplaatst:\n\n{title}\n{link}")
    msg['Subject'] = "Nieuwe blog op FBN Design"
    msg['From'] = email_user
    msg['To'] = notify_email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(email_user, email_pass)
            smtp.send_message(msg)
            print("📧 Mail verzonden naar:", notify_email)
    except Exception as e:
        print("❌ Fout bij e-mail verzenden:", e)
else:
    print(f"❌ Mislukt: {res.status_code}\n{res.text}")
