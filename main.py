wp_user = os.environ['WP_USER']
wp_password = os.environ['WP_APP_PASSWORD']

# SEO TITEL OPTIES (uniek, zonder datum)
title_options = [
    "Lokale SEO-kansen in Zuid-Holland benutten",
    "Zo vergroot je online zichtbaarheid in Zuid-Holland",
    "Meer B2B-leads met SEO in Rotterdam",
    "Waarom bedrijven in Zuid-Holland investeren in zoekmachineoptimalisatie",
    "De kracht van contentmarketing voor MKB Zuid-Holland",
    "Hoe jij meer klanten trekt via Google in Zuid-Holland"
    "Waarom SEO essentieel is voor bedrijven in Zuid-Holland",
    "Lokale zichtbaarheid verbeteren als ondernemer in Zuid-Holland",
    "Contentstrategie voor MKB in Zuid-Holland"
]
title = random.choice(title_options)

@@ -26,8 +25,8 @@
    "Content-Type": "application/json"
}

# === MEDIA AANMAKEN EN TERUGGEVEN ALS BLOCK EN HTML TAG ===
def generate_and_upload(prompt, alt):
# === HELPER: AFBEELDING UPLOADEN ===
def upload_image(prompt, alt):
    img_data = requests.get(f"https://source.unsplash.com/800x600/?{prompt}").content
    filename = f"{prompt.replace(' ', '_')}.jpg"
    with open(filename, 'wb') as f:
@@ -46,71 +45,107 @@ def generate_and_upload(prompt, alt):

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
        return media['id'], media['source_url']
    return None, ''

# === CONTENT BLOKKEN ===
content_blocks = []
html_content = ""

intro_html = """<p><strong>Wil jij als ondernemer in Zuid-Holland meer uit online marketing halen?</strong> Dan is SEO geen luxe meer, maar noodzaak. In dit artikel lees je hoe je vindbaarheid en conversie vergroot.</p>"""
blocks.append({"blockName": "core/paragraph", "attrs": {}, "innerHTML": intro_html, "innerContent": [intro_html]})
intro_html = """
<p><strong>Wil jij als ondernemer in Zuid-Holland meer uit online marketing halen?</strong>
Dan is SEO geen luxe meer, maar noodzaak. In dit artikel lees je hoe je vindbaarheid en conversie vergroot.</p>
"""
content_blocks.append({"blockName": "core/paragraph", "attrs": {}, "innerHTML": intro_html, "innerContent": [intro_html]})
html_content += intro_html

koppen = [
    "Lokale SEO: scoor in je regio",
    "Content die converteert",
    "Techniek telt mee"
]
teksten = [
    ("1. Lokale SEO: scoor in je regio", "Gebruik lokale zoekwoorden zoals 'SEO bureau Rotterdam' of 'marketingbureau Den Haag'. Zorg dat je Google bedrijfsprofiel geoptimaliseerd is."),
    ("2. Content die converteert", "Publiceer waardevolle content die inspeelt op vragen van jouw doelgroep. Denk aan checklists, blogs of gratis downloads."),
    ("3. Techniek telt mee", "Een snelle website en duidelijke structuur helpen Google én je bezoeker. Gebruik tools als PageSpeed Insights om verbeterpunten te vinden.")
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
    heading_html = f"<h3>{koppen[i]}</h3>"
    paragraph_html = f"<p>{teksten[i]}</p>"
    image_id, image_url = upload_image(prompts[i], alts[i])

    if i == 0 and image_id:
        featured_media_id = image_id

    # Media text block
    media_block = {
        "blockName": "core/media-text",
        "attrs": {
            "mediaId": image_id,
            "mediaType": "image",
            "mediaUrl": image_url,
            "verticalAlignment": "center"
        },
        "innerBlocks": [
            {
                "blockName": "core/image",
                "attrs": {"id": image_id, "alt": alts[i]},
                "innerHTML": f"<img src=\"{image_url}\" alt=\"{alts[i]}\" />",
                "innerContent": [f"<img src=\"{image_url}\" alt=\"{alts[i]}\" />"]
            },
            {
                "blockName": "core/paragraph",
                "attrs": {},
                "innerHTML": heading_html + paragraph_html,
                "innerContent": [heading_html + paragraph_html]
            }
        ],
        "innerHTML": "",
        "innerContent": []
    }
    content_blocks.append(media_block)
    html_content += heading_html + paragraph_html + f'<img src="{image_url}" alt="{alts[i]}">'  # fallback

outro_html = """
<p><strong>Klaar om hoger te ranken en meer leads te scoren?</strong>
FBN Marketing helpt bedrijven in Zuid-Holland groeien via SEO.</p>
"""
content_blocks.append({"blockName": "core/paragraph", "attrs": {}, "innerHTML": outro_html, "innerContent": [outro_html]})
html_content += outro_html

# === POST OPSTELLEN ===
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
    "blocks": blocks,
    "blocks": content_blocks,
    "featured_media": featured_media_id,
    "meta": {
        "yoast_title": title,
        "yoast_meta": f"{title} - SEO tips voor ondernemers in Zuid-Holland.",
        "yoast_focuskw": "SEO Zuid-Holland"
    }
    "meta": seo_meta
}

r = requests.post(f"{wp_url}/wp-json/wp/v2/posts", headers=headers, json=post_data)
if r.status_code == 201:
    print("✅ Versie 3.8 geplaatst – fallback HTML toegevoegd + afbeeldingen geforceerd")
res = requests.post(f"{wp_url}/wp-json/wp/v2/posts", headers=headers, json=post_data)

if res.status_code == 201:
    print("✅ Post succesvol gepubliceerd met layout en afbeeldingen.")
else:
    print(f"❌ Mislukt: {r.status_code}\n{r.text}")
    print(f"❌ Publiceren mislukt: {res.status_code}\n{res.text}")
