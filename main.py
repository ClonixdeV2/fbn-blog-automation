import requests
import base64
import os
import random
import smtplib
from email.mime.text import MIMEText

# === CONFIG ===
wp_url = os.environ['WP_URL']
wp_user = os.environ['WP_USER']
wp_password = os.environ['WP_APP_PASSWORD']

# Email info
notify_email = os.environ['EMAIL_NOTIFY']
email_user = os.environ['EMAIL_USER']
email_pass = os.environ['EMAIL_PASS']

# === TITELS & STRUCTUUR ===
title_options = [
    "Zo verbeter je je online zichtbaarheid in Zuid-Holland",
    "Waarom SEO cruciaal is voor ondernemers in Zuid-Holland",
    "Een contentstrategie die werkt voor MKB in Zuid-Holland",
    "Lokale marketingtips voor bedrijven in Rotterdam & omgeving",
    "Meer leads en zichtbaarheid via SEO: zo pak je het aan"
]
title = random.choice(title_options)

# AUTH
auth = base64.b64encode(f"{wp_user}:{wp_password}".encode()).decode("utf-8")
headers = {
    "Authorization": f"Basic {auth}",
    "Content-Type": "application/json"
}

# === SEO BLOG OPBOUWEN ===
intro = """
<p><strong>Als ondernemer in Zuid-Holland weet je hoe belangrijk het is om online gevonden te worden.</strong>
In deze blog leer je hoe je met slimme SEO en contentmarketing meer verkeer én klanten aantrekt.</p>
"""

h1 = "<h3>Wat is lokale SEO precies?</h3>"
p1 = "<p>Lokale SEO richt zich op het vindbaar maken van je bedrijf in je directe omgeving. Denk aan zoekopdrachten als 'marketingbureau Rotterdam' of 'webdesign Den Haag'. Door je website en content lokaal te optimaliseren, sta je sneller bovenaan in Google voor mensen in jouw regio.</p>"

h2 = "<h3>Content die vertrouwen opbouwt</h3>"
p2 = "<p>Publiceer regelmatig waardevolle content die inspeelt op vragen van jouw doelgroep. Denk aan blogs, checklists of klantverhalen. Vermijd oppervlakkigheid: Google beloont diepgang en originaliteit. Schrijf minimaal 600 woorden en gebruik relevante zoekwoorden, zoals 'SEO Zuid-Holland' of 'online marketing MKB'.</p>"

h3 = "<h3>Techniek en snelheid: de onzichtbare helden</h3>"
p3 = "<p>Een snelle, technisch goed gebouwde website is essentieel. Zorg voor een mobielvriendelijk ontwerp, schone code en snelle laadtijden. Tools zoals Google PageSpeed Insights en GTmetrix helpen je verbeterpunten te vinden. Vergeet ook de juiste structuur van je headings (H1, H2, H3) niet.</p>"

h4 = "<h3>Gebruik Google Mijn Bedrijf</h3>"
p4 = "<p>Een goed ingevuld Google Business-profiel maakt je zichtbaar in Google Maps én in lokale zoekresultaten. Vraag klanten om reviews, upload foto’s en zorg dat je bedrijfsinformatie actueel blijft. Dit versterkt je lokale SEO enorm.</p>"

outro = """
<p><strong>Wil jij hoger in Google komen en meer klanten aantrekken?</strong>
FBN Marketing helpt bedrijven in Zuid-Holland met effectieve SEO en contentstrategie. Neem contact op voor een vrijblijvende scan van je online vindbaarheid.</p>
"""

html_content = intro + h1 + p1 + h2 + p2 + h3 + p3 + h4 + p4 + outro

# === YOAST META ===
seo_meta = {
    "yoast_title": title,
    "yoast_meta": f"{title} - Praktische SEO tips voor ondernemers in Zuid-Holland.",
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
    post_link = post['link']
    print("✅ Blog gepubliceerd: ", post_link)

    # === MAIL VERSTUREN ===
    msg = MIMEText(f"Er is een nieuwe blog geplaatst op FBN Design:\n\n{title}\n{post_link}")
    msg['Subject'] = "Nieuwe blog op FBN Design"
    msg['From'] = email_user
    msg['To'] = notify_email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(email_user, email_pass)
            smtp.send_message(msg)
            print("📧 Mail verstuurd naar:", notify_email)
    except Exception as e:
        print("❌ Mail kon niet worden verstuurd:", e)
else:
    print(f"❌ Mislukt: {res.status_code}\n{res.text}")
name: Blog plaatsen

on:
  workflow_dispatch:

jobs:
  post_blog:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install requests

      - name: Blog plaatsen
        run: python main.py
        env:
          WP_URL: ${{ secrets.WP_URL }}
          WP_USER: ${{ secrets.WP_USER }}
          WP_APP_PASSWORD: ${{ secrets.WP_APP_PASSWORD }}
          EMAIL_USER: ${{ secrets.EMAIL_USER }}
          EMAIL_PASS: ${{ secrets.EMAIL_PASS }}
          EMAIL_NOTIFY: ${{ secrets.EMAIL_NOTIFY }}
