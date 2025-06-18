import requests
import base64
import os
import random
from datetime import datetime

# === CONFIG ===
wp_url = os.environ['WP_URL']
wp_user = os.environ['WP_USER']
wp_password = os.environ['WP_APP_PASSWORD']

title_options = [
    "Zo vergroot je online zichtbaarheid in Zuid-Holland",
    "Meer B2B-leads met SEO in Rotterdam",
    "Waarom SEO essentieel is voor bedrijven in Zuid-Holland",
    "Lokale zichtbaarheid verbeteren als ondernemer in Zuid-Holland",
    "Contentstrategie voor MKB in Zuid-Holland"
]
title = random.choice(title_options)

# AUTH
auth = base64.b64encode(f"{wp_user}:{wp_password}".encode()).decode("utf-8")
headers = {
    "Authorization": f"Basic {auth}",
    "Content-Type": "application/json"
}

# === HELPER: AFBEELDING UPLOADEN ===
def upload_image(prompt, alt):
    img_data = requests.get(f"https://source.unsplash.com/800x600/?{prompt}").content
    filename = f"{prompt.replace(' ', '_')}.jpg"
    with open(filename, 'wb') as f:
        f.write(img_data)

    upload_headers = {
        "Authorization": f"Basic {auth}",
        "Content-Disposition": f"attachment; filename={filename}",
        "Content-Type": "image/jpeg"
    }

    with open(filename, 'rb') as f:
        res = requests.post(f"{wp_url}/wp-json/wp/v2/media", headers=upload_headers, data=f.read())

    os.remove(filename)

    if res.status_code == 201:
        media = res.json()
        return media['id'], media['source_url']
    return None, ''

# === CONTENT OPBOUWEN ALS PURE HTML ===
html_content = ""

intro_html = """
<p><strong>Wil jij als ondernemer in Zuid-Holland meer uit online marketing halen?</strong>
Dan is SEO geen luxe meer, maar noodzaak. In dit artikel lees je hoe je vindbaarheid en conversie vergroot.</p>
"""
html_content += intro_html

koppen = [
    "Lokale SEO: scoor in je regio",
    "Content die converteert",
    "Techniek telt mee"
]
teksten = [
    "Gebruik lokale zoekwoorden zoals 'SEO bureau Rotterdam' of 'marketingbureau Den Haag'. Zorg dat je Google bedrijfsprofiel geoptimaliseerd is.",
    "Publiceer waardevolle content die inspeelt op vragen van jouw doelgroep. Denk aan checklists, blogs of gratis downloads.",
    "Een snelle website en duidelijke structuur helpen Google én je bezoeker. Gebruik tools als PageSpeed Insights om verbeterpunten te vinden."
]
prompts = [
    "seo rotterdam",
    "content marketing",
    "technical seo"
]
alts = [
    "SEO Rotterdam",
    "Contentstrategie B2B",
    "Technische optimalisatie"
]

featured_media_id = None

for i in range(3):
    heading_html = f"<h3>{koppen[i]}</h3>"
    paragraph_html = f"<p>{teksten[i]}</p>"
    image_id, image_url = upload_image(prompts[i], alts[i])

    if i == 0 and image_id:
        featured_media_id = image_id

    html_content += heading_html + paragraph_html + f'<img src="{image_url}" alt="{alts[i]}"><br>'

outro_html = """
<p><strong>Klaar om hoger te ranken en meer leads te scoren?</strong>
FBN Marketing helpt bedrijven in Zuid-Holland groeien via SEO.</p>
"""
html_content += outro_html

# === YOAST SEO META ===
seo_meta = {
    "yoast_title": title,
    "yoast_meta": f"{title} - SEO tips voor ondernemers in Zuid-Holland.",
    "yoast_focuskw": "SEO Zuid-Holland"
}

# === POST VERSTUREN ===
post_data = {
    "title": title,
    "status": "publish",
    "content": html_content,
    "featured_media": featured_media_id,
    "meta": seo_meta
}

res = requests.post(f"{wp_url}/wp-json/wp/v2/posts", headers=headers, json=post_data)

if res.status_code == 201:
    print("✅ Post succesvol gepubliceerd met tekst, afbeeldingen en layout.")
else:
    print(f"❌ Publiceren mislukt: {res.status_code}\n{res.text}")
