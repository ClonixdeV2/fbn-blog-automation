import requests
import base64
import os
import random
from datetime import datetime

# === CONFIG ===
wp_url = os.environ['WP_URL']
wp_user = os.environ['WP_USER']
wp_password = os.environ['WP_APP_PASSWORD']

# SEO TITEL OPTIES (uniek, zonder datum)
title_options = [
    "Lokale SEO-kansen in Zuid-Holland benutten",
    "Meer B2B-leads met SEO in Rotterdam",
    "Waarom bedrijven in Zuid-Holland investeren in zoekmachineoptimalisatie",
    "De kracht van contentmarketing voor MKB Zuid-Holland",
    "Hoe jij meer klanten trekt via Google in Zuid-Holland"
]
title = random.choice(title_options)

# AUTH
auth = base64.b64encode(f"{wp_user}:{wp_password}".encode()).decode("utf-8")
headers = {
    "Authorization": f"Basic {auth}",
    "Content-Type": "application/json"
}

# === MEDIA AANMAKEN EN TERUGGEVEN ALS BLOCK EN HTML TAG ===
def generate_and_upload(prompt, alt):
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
        img_url = media['source_url']
        media_id = media['id']
        block = {
            "blockName": "core/image",
            "attrs": {"id": media_id, "alt": alt},
            "innerHTML": f"<img src=\"{img_url}\" alt=\"{alt}\"/>",
            "innerContent": [f"<img src=\"{img_url}\" alt=\"{alt}\"/>"]
        }
        html_tag = f'<img src="{img_url}" alt="{alt}"/>'
        return block, media_id, html_tag
    else:
        return None, None, ''

# === BLOKKEN STRUCTUUR OPBOUWEN ===
blocks = []
html_content = ""

intro_html = """<p><strong>Wil jij als ondernemer in Zuid-Holland meer uit online marketing halen?</strong> Dan is SEO geen luxe meer, maar noodzaak. In dit artikel lees je hoe je vindbaarheid en conversie vergroot.</p>"""
blocks.append({"blockName": "core/paragraph", "attrs": {}, "innerHTML": intro_html, "innerContent": [intro_html]})
html_content += intro_html

teksten = [
    ("1. Lokale SEO: scoor in je regio", "Gebruik lokale zoekwoorden zoals 'SEO bureau Rotterdam' of 'marketingbureau Den Haag'. Zorg dat je Google bedrijfsprofiel geoptimaliseerd is."),
    ("2. Content die converteert", "Publiceer waardevolle content die inspeelt op vragen van jouw doelgroep. Denk aan checklists, blogs of gratis downloads."),
    ("3. Techniek telt mee", "Een snelle website en duidelijke structuur helpen Google én je bezoeker. Gebruik tools als PageSpeed Insights om verbeterpunten te vinden.")
]

prompts = ["seo rotterdam", "content marketing b2b", "technical seo"]
alts = ["SEO Rotterdam tips", "Contentmarketing Zuid-Holland", "SEO technische optimalisatie"]

featured_media_id = None

for i in range(3):
    heading, text = teksten[i]
    tekst_html = f"<h3>{heading}</h3><p>{text}</p>"
    blocks.append({"blockName": "core/paragraph", "attrs": {}, "innerHTML": tekst_html, "innerContent": [tekst_html]})
    html_content += tekst_html

    image_block, media_id, html_tag = generate_and_upload(prompts[i], alts[i])
    if image_block:
        blocks.append(image_block)
        html_content += html_tag
        if i == 0:
            featured_media_id = media_id

outro_html = """<p><strong>Klaar om hoger te ranken en meer leads te scoren?</strong> FBN Marketing helpt bedrijven in Zuid-Holland groeien via SEO.</p>"""
blocks.append({"blockName": "core/paragraph", "attrs": {}, "innerHTML": outro_html, "innerContent": [outro_html]})
html_content += outro_html

# === POST OPSTELLEN ===
post_data = {
    "title": title,
    "status": "publish",
    "content": html_content,
    "blocks": blocks,
    "featured_media": featured_media_id,
    "meta": {
        "yoast_title": title,
        "yoast_meta": f"{title} - SEO tips voor ondernemers in Zuid-Holland.",
        "yoast_focuskw": "SEO Zuid-Holland"
    }
}

r = requests.post(f"{wp_url}/wp-json/wp/v2/posts", headers=headers, json=post_data)
if r.status_code == 201:
    print("✅ Versie 3.8 geplaatst – fallback HTML toegevoegd + afbeeldingen geforceerd")
else:
    print(f"❌ Mislukt: {r.status_code}\n{r.text}")
