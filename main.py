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

# === AUTH HEADER ===
wp_auth = base64.b64encode(f"{wp_user}:{wp_password}".encode()).decode("utf-8")
headers = {
    "Authorization": f"Basic {wp_auth}",
    "Content-Type": "application/json"
}

# === LOKALE AI-AFBEELDING (DALL-E via placeholder) ===
def generate_image_file(prompt):
    dalle_url = f"https://source.unsplash.com/800x600/?{prompt}"
    img_data = requests.get(dalle_url).content
    filename = f"image_{prompt.replace(' ', '_')}.jpg"
    with open(filename, 'wb') as f:
        f.write(img_data)
    return filename

def upload_media(filename, alt_text):
    media_headers = {
        "Authorization": f"Basic {wp_auth}",
        "Content-Disposition": f"attachment; filename={filename}",
        "Content-Type": "image/jpeg"
    }
    with open(filename, 'rb') as f:
        img_data = f.read()
    response = requests.post(f"{wp_url}/wp-json/wp/v2/media", headers=media_headers, data=img_data)
    if response.status_code == 201:
        return response.json()['source_url'], response.json()['id']
    return None, None

# Genereer & upload 3 afbeeldingen
prompts = ["seo rotterdam", "content marketing b2b", "technical seo"]
alts = ["SEO Rotterdam tips", "Contentmarketing Zuid-Holland", "SEO technische optimalisatie"]
img_urls = []
img_ids = []

for i in range(3):
    file = generate_image_file(prompts[i])
    url, media_id = upload_media(file, alts[i])
    img_urls.append(url)
    img_ids.append(media_id)
    os.remove(file)

# === HTML-CONTENT MET INGESLOTEN IMG TAGS ===
content = f"""
<p><strong>Wil jij als ondernemer in Zuid-Holland meer uit online marketing halen?</strong> Dan is SEO geen luxe meer, maar noodzaak. In dit artikel lees je hoe je vindbaarheid en conversie vergroot.</p>

<div style='display:flex;flex-wrap:wrap;align-items:center;margin:40px 0;'>
  <div style='flex:1;padding:10px;'>
    <h3>1. Lokale SEO: scoor in je regio</h3>
    <p>Gebruik lokale zoekwoorden zoals 'SEO bureau Rotterdam' of 'marketingbureau Den Haag'. Zorg dat je Google bedrijfsprofiel geoptimaliseerd is.</p>
  </div>
  <div style='flex:1;padding:10px;'>
    <img src='{img_urls[0]}' alt='SEO Rotterdam tips' style='max-width:100%;border-radius:8px;'>
  </div>
</div>

<div style='display:flex;flex-wrap:wrap;align-items:center;margin:40px 0;flex-direction:row-reverse;'>
  <div style='flex:1;padding:10px;'>
    <h3>2. Content die converteert</h3>
    <p>Publiceer waardevolle content die inspeelt op vragen van jouw doelgroep. Denk aan checklists, blogs of gratis downloads.</p>
  </div>
  <div style='flex:1;padding:10px;'>
    <img src='{img_urls[1]}' alt='Contentmarketing Zuid-Holland' style='max-width:100%;border-radius:8px;'>
  </div>
</div>

<div style='display:flex;flex-wrap:wrap;align-items:center;margin:40px 0;'>
  <div style='flex:1;padding:10px;'>
    <h3>3. Techniek telt mee</h3>
    <p>Een snelle website en duidelijke structuur helpen Google én je bezoeker. Gebruik tools als PageSpeed Insights om verbeterpunten te vinden.</p>
  </div>
  <div style='flex:1;padding:10px;'>
    <img src='{img_urls[2]}' alt='SEO technische optimalisatie' style='max-width:100%;border-radius:8px;'>
  </div>
</div>

<p><strong>Klaar om hoger te ranken en meer leads te scoren?</strong> FBN Marketing helpt bedrijven in Zuid-Holland groeien via SEO.</p>
"""

# === POSTEN ===
post_data = {
    "title": title,
    "content": content,
    "status": "publish",
    "featured_media": img_ids[0],
    "meta": {
        "yoast_title": title,
        "yoast_meta": f"{title} - SEO tips voor ondernemers in Zuid-Holland.",
        "yoast_focuskw": "SEO Zuid-Holland"
    }
}

response = requests.post(f"{wp_url}/wp-json/wp/v2/posts", headers=headers, json=post_data)
if response.status_code == 201:
    print("✅ Blog met AI-afbeeldingen succesvol gepubliceerd")
else:
    print("❌ Fout bij plaatsen:", response.status_code, response.text)
