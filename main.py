import requests
import base64
import os
import random
from datetime import datetime

# === CONFIG ===
wp_url = os.environ['WP_URL']
wp_user = os.environ['WP_USER']
wp_password = os.environ['WP_APP_PASSWORD']

# Nieuwe SEO-titels zonder datum
title_options = [
    "Zo vergroot je online zichtbaarheid in Zuid-Holland",
    "B2B marketing in Rotterdam: dit werkt wél in 2025",
    "SEO-tips voor ondernemers in Zuid-Holland",
    "Hoe MKB-bedrijven in Zuid-Holland scoren met SEO",
    "Leadgeneratie via Google: kansen voor jouw bedrijf"
]
title = random.choice(title_options)

# Afbeelding gerelateerde alt teksten
alt_texts = [
    "SEO tips voor B2B Zuid-Holland",
    "Lokale vindbaarheid Rotterdam",
    "Marketingstrategie voor ondernemers"
]

# Afbeelding ophalen en uploaden
img_urls = []
img_ids = []
for i in range(3):
    img_data = requests.get("https://source.unsplash.com/600x400/?seo,marketing,business").content
    img_headers = {
        "Authorization": f"Basic {base64.b64encode(f'{wp_user}:{wp_password}'.encode()).decode('utf-8')}",
        "Content-Disposition": f"attachment; filename=seo_img_{i}.jpg",
        "Content-Type": "image/jpeg"
    }
    res = requests.post(f"{wp_url}/wp-json/wp/v2/media", headers=img_headers, data=img_data)
    if res.status_code == 201:
        img_json = res.json()
        img_urls.append(img_json['source_url'])
        img_ids.append(img_json['id'])
    else:
        img_urls.append("")
        img_ids.append(None)

# HTML content met geforceerde structuur
content = f"""
<p><strong>Als ondernemer in Zuid-Holland wil je niet alleen aanwezig zijn online, maar ook vindbaar.</strong> SEO helpt je structureel klanten aan te trekken, vooral in een B2B-context. In dit artikel leer je hoe.</p>

<div style='display:flex;flex-wrap:wrap;align-items:center;margin:40px 0;'>
  <div style='flex:1;padding:10px;'>
    <h3>1. Focus op lokale SEO</h3>
    <p>Klanten zoeken op termen als 'SEO bureau Rotterdam' of 'marketingbedrijf Zuid-Holland'. Optimaliseer je Google Bedrijfsprofiel en gebruik lokale landingspagina's.</p>
  </div>
  <div style='flex:1;padding:10px;'>
    <img src='{img_urls[0]}' alt='{alt_texts[0]}' style='max-width:100%;height:auto;border-radius:8px;'>
  </div>
</div>

<div style='display:flex;flex-wrap:wrap;align-items:center;margin:40px 0;flex-direction:row-reverse;'>
  <div style='flex:1;padding:10px;'>
    <h3>2. Creëer waardevolle content</h3>
    <p>Goede content scoort, zeker als je de juiste zoektermen gebruikt. Denk aan blogs, gidsen of cases die inspelen op je doelgroep.</p>
  </div>
  <div style='flex:1;padding:10px;'>
    <img src='{img_urls[1]}' alt='{alt_texts[1]}' style='max-width:100%;height:auto;border-radius:8px;'>
  </div>
</div>

<div style='display:flex;flex-wrap:wrap;align-items:center;margin:40px 0;'>
  <div style='flex:1;padding:10px;'>
    <h3>3. Meer leads via conversie-optimalisatie</h3>
    <p>SEO haalt bezoekers, maar CRO zorgt voor klanten. Zorg voor een sterke landingspagina, duidelijke CTA en snelle laadtijd.</p>
  </div>
  <div style='flex:1;padding:10px;'>
    <img src='{img_urls[2]}' alt='{alt_texts[2]}' style='max-width:100%;height:auto;border-radius:8px;'>
  </div>
</div>

<p><strong>Wil je dit ook voor jouw bedrijf? Neem contact op met FBN Marketing en laat je online zichtbaarheid groeien.</strong></p>
"""

# AUTH
headers = {
    "Authorization": f"Basic {base64.b64encode(f'{wp_user}:{wp_password}'.encode()).decode('utf-8')}",
    "Content-Type": "application/json"
}

# POST
post_data = {
    "title": title,
    "content": content,
    "status": "publish",
    "featured_media": img_ids[0] if img_ids[0] else None,
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
