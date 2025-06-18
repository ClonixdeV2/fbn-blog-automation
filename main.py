import requests
import base64
import os
import random
from datetime import datetime

# === CONFIG ===
wp_url = os.environ['WP_URL']
wp_user = os.environ['WP_USER']
wp_password = os.environ['WP_APP_PASSWORD']

# AI gegenereerde SEO-titels gericht op Zuid-Holland B2B zoekopdrachten
title_options = [
    "Zo vergroot je online zichtbaarheid in Zuid-Holland",
    "B2B marketing in Rotterdam: dit werkt wél in 2025",
    "SEO-tips voor ondernemers in Zuid-Holland",
    "Hoe MKB-bedrijven in Zuid-Holland scoren met SEO",
    "Leadgeneratie via Google: kansen voor jouw bedrijf"
]
title = random.choice(title_options)
alt_texts = [
    "SEO tips voor B2B Zuid-Holland",
    "Lokale vindbaarheid Rotterdam",
    "Marketingstrategie voor ondernemers",
    "Google optimalisatie tips",
    "Meer leads met SEO in 2025"
]

def fetch_image():
    url = "https://source.unsplash.com/600x400/?seo,marketing,business"
    return requests.get(url).content

def upload_image(image_data, alt):
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{wp_user}:{wp_password}'.encode()).decode('utf-8')}",
        "Content-Disposition": "attachment; filename=img.jpg",
        "Content-Type": "image/jpeg"
    }
    r = requests.post(f"{wp_url}/wp-json/wp/v2/media", headers=headers, data=image_data)
    if r.status_code == 201:
        return r.json()['source_url'], r.json()['id']
    return None, None

# Afbeeldingen ophalen en uploaden
images = []
for i in range(3):
    img_data = fetch_image()
    img_url, img_id = upload_image(img_data, alt_texts[i])
    images.append((img_url, alt_texts[i]))

# Content structuur: intro + 3 blokken tekst/beeld
intro = "<p><strong>Als ondernemer in Zuid-Holland wil je niet alleen aanwezig zijn online, maar ook vindbaar.</strong> SEO helpt je structureel klanten aan te trekken, vooral in een B2B-context. In dit artikel leer je hoe.</p>"

blocks = [
    [
        "<h3>1. Focus op lokale SEO</h3><p>Klanten zoeken op termen als 'SEO bureau Rotterdam' of 'marketingbedrijf Zuid-Holland'. Optimaliseer je Google Bedrijfsprofiel en gebruik lokale landingspagina's.</p>",
        f'<img src="{images[0][0]}" alt="{images[0][1]}" style="max-width:400px;border-radius:8px;">',
        False
    ],
    [
        "<h3>2. Creëer waardevolle content</h3><p>Goede content scoort, zeker als je de juiste zoektermen gebruikt. Denk aan blogs, gidsen of cases die inspelen op je doelgroep.</p>",
        f'<img src="{images[1][0]}" alt="{images[1][1]}" style="max-width:400px;border-radius:8px;">',
        True
    ],
    [
        "<h3>3. Meer leads via conversie-optimalisatie</h3><p>SEO haalt bezoekers, maar CRO zorgt voor klanten. Zorg voor een sterke landingspagina, duidelijke CTA en snelle laadtijd.</p>",
        f'<img src="{images[2][0]}" alt="{images[2][1]}" style="max-width:400px;border-radius:8px;">',
        False
    ]
]

body = intro
for text, img, reverse in blocks:
    body += f'<div style="display:flex;gap:30px;align-items:center;flex-direction:{"row-reverse" if reverse else "row"};margin:40px 0;">'
    body += f'<div style="flex:1">{text}</div>'
    body += f'<div style="flex:1">{img}</div>'
    body += '</div>'

body += "<p><strong>Wil je dit ook voor jouw bedrijf? Neem contact op met FBN Marketing en laat je online zichtbaarheid groeien.</strong></p>"

# === AUTH & HEADERS ===
token = base64.b64encode(f"{wp_user}:{wp_password}".encode()).decode("utf-8")
headers = {
    "Authorization": f"Basic {token}",
    "Content-Type": "application/json"
}

# === POST ===
post_data = {
    "title": title,
    "content": body,
    "status": "publish",
    "featured_media": images[0][1] if images[0][1] else None,
    "meta": {
        "yoast_title": title,
        "yoast_meta": f"{title} - SEO & marketing tips voor ondernemers in Zuid-Holland.",
        "yoast_focuskw": "SEO Zuid-Holland"
    }
}

r = requests.post(f"{wp_url}/wp-json/wp/v2/posts", headers=headers, json=post_data)
if r.status_code == 201:
    print("✅ Blog succesvol geplaatst!")
else:
    print(f"❌ Mislukt: {r.status_code}\n{r.text}")
