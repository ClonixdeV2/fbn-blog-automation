import requests
import base64
import os
from datetime import datetime

# === CONFIG ===
wp_url = os.environ['WP_URL']
wp_user = os.environ['WP_USER']
wp_password = os.environ['WP_APP_PASSWORD']

title = "7 SEO-strategieën die B2B bedrijven in 2025 winst opleveren"
image_url = "https://source.unsplash.com/960x640/?seo,marketing,business"
alt_text = "SEO-strategieën voor B2B in 2025"

content = f"""
<p><strong>SEO is in 2025 geen optie meer, maar een noodzaak.</strong> Vooral in B2B-markten waar concurrentie hevig is en beslissers snel willen schakelen.</p>

<img src=\"{image_url}\" alt=\"{alt_text}\" style=\"max-width:100%;height:auto;margin:20px 0;\"/>

<h3>1. Zoekwoordonderzoek met intentie</h3>
<p>Gebruik tools zoals SEMrush of Ubersuggest om niet alleen volume, maar <strong>zoekintentie</strong> te begrijpen. B2B-klanten zoeken anders dan consumenten.</p>

<h3>2. Optimaliseer voor conversie</h3>
<p>Het is niet genoeg om bezoekers te trekken. Zet in op <strong>leadgeneratie</strong> door duidelijke CTA's en downloadbare whitepapers.</p>

<h3>3. Lokale SEO, ook voor B2B</h3>
<p>Zelfs als je nationaal werkt, kan lokaal gevonden worden doorslaggevend zijn. Zorg dat je bedrijfsprofiel klopt en lokaal scoort.</p>

<h3>4. Techniek = fundering</h3>
<p>Een trage site of kapotte links zijn SEO-killers. Gebruik Lighthouse of PageSpeed Insights en fix fouten.</p>

<h3>5. EAT: Expertise, Authoritativeness, Trust</h3>
<p>Laat zien dat je expert bent. Publiceer blogs, cases en artikelen die autoriteit uitstralen.</p>

<h3>6. Linkbuilding blijft key</h3>
<p>Externe verwijzingen van relevante websites maken je domein sterker. Denk aan gastblogs of vakportalen.</p>

<h3>7. Contentconsistentie</h3>
<p>Google beloont websites die <em>regelmatig</em> publiceren. Zoals deze blog dus. 😉</p>

<p><strong>Conclusie:</strong> Begin vandaag. Of bel FBN Marketing, dan regelen wij het.</p>
"""

# === AUTH ===
token = base64.b64encode(f"{wp_user}:{wp_password}".encode()).decode("utf-8")
headers = {
    "Authorization": f"Basic {token}",
    "Content-Type": "application/json"
}

# === AFBEELDING OPHALEN EN UPLOADEN ===
image_data = requests.get(image_url).content
media = requests.post(
    f"{wp_url}/wp-json/wp/v2/media",
    headers={**headers, "Content-Disposition": "attachment; filename=seo.jpg"},
    data=image_data
)

if media.status_code == 201:
    image_id = media.json()['id']
else:
    image_id = None

# === BLOG PLAATSEN ===
post_data = {
    "title": title,
    "content": content,
    "status": "publish",
    "featured_media": image_id if image_id else None
}

r = requests.post(f"{wp_url}/wp-json/wp/v2/posts", headers=headers, json=post_data)

if r.status_code == 201:
    print("✅ Blog succesvol geplaatst!")
else:
    print(f"❌ Mislukt: {r.status_code}\n{r.text}")
