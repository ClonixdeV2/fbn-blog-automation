import requests
import base64
import os
import random
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

# === CONFIG ===
wp_url = os.environ['WP_URL']
wp_user = os.environ['WP_USER']
wp_password = os.environ['WP_APP_PASSWORD']

# Email info
notify_email = "fabianbaartman5@gmail.com"

# === TITELS & STRUCTUUR ===
title_options = [
    "Zo vergroot je online zichtbaarheid in Zuid-Holland",
    "Meer B2B-leads met SEO in Rotterdam",
    "Waarom SEO essentieel is voor bedrijven in Zuid-Holland",
    "Lokale zichtbaarheid verbeteren als ondernemer in Zuid-Holland",
    "Contentstrategie voor MKB in Zuid-Holland"
    "Zo verbeter je je online zichtbaarheid in Zuid-Holland",
    "Waarom SEO cruciaal is voor ondernemers in Zuid-Holland",
    "Een contentstrategie die werkt voor MKB in Zuid-Holland",
    "Lokale marketingtips voor bedrijven in Rotterdam & omgeving",
    "Meer leads en zichtbaarheid via SEO: zo pak je het aan"
]
title = random.choice(title_options)

@@ -25,96 +30,66 @@
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
# === SEO BLOG OPBOUWEN ===
intro = """
<p><strong>Als ondernemer in Zuid-Holland weet je hoe belangrijk het is om online gevonden te worden.</strong>
In deze blog leer je hoe je met slimme SEO en contentmarketing meer verkeer én klanten aantrekt.</p>
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
h1 = "<h3>Wat is lokale SEO precies?</h3>"
p1 = "<p>Lokale SEO richt zich op het vindbaar maken van je bedrijf in je directe omgeving. Denk aan zoekopdrachten als 'marketingbureau Rotterdam' of 'webdesign Den Haag'. Door je website en content lokaal te optimaliseren, sta je sneller bovenaan in Google voor mensen in jouw regio.</p>"

for i in range(3):
    heading_html = f"<h3>{koppen[i]}</h3>"
    paragraph_html = f"<p>{teksten[i]}</p>"
    image_id, image_url = upload_image(prompts[i], alts[i])
h2 = "<h3>Content die vertrouwen opbouwt</h3>"
p2 = "<p>Publiceer regelmatig waardevolle content die inspeelt op vragen van jouw doelgroep. Denk aan blogs, checklists of klantverhalen. Vermijd oppervlakkigheid: Google beloont diepgang en originaliteit. Schrijf minimaal 600 woorden en gebruik relevante zoekwoorden, zoals 'SEO Zuid-Holland' of 'online marketing MKB'.</p>"

    if i == 0 and image_id:
        featured_media_id = image_id
h3 = "<h3>Techniek en snelheid: de onzichtbare helden</h3>"
p3 = "<p>Een snelle, technisch goed gebouwde website is essentieel. Zorg voor een mobielvriendelijk ontwerp, schone code en snelle laadtijden. Tools zoals Google PageSpeed Insights en GTmetrix helpen je verbeterpunten te vinden. Vergeet ook de juiste structuur van je headings (H1, H2, H3) niet.</p>"

    html_content += heading_html + paragraph_html + f'<img src="{image_url}" alt="{alts[i]}"><br>'
h4 = "<h3>Gebruik Google Mijn Bedrijf</h3>"
p4 = "<p>Een goed ingevuld Google Business-profiel maakt je zichtbaar in Google Maps én in lokale zoekresultaten. Vraag klanten om reviews, upload foto’s en zorg dat je bedrijfsinformatie actueel blijft. Dit versterkt je lokale SEO enorm.</p>"

outro_html = """
<p><strong>Klaar om hoger te ranken en meer leads te scoren?</strong>
FBN Marketing helpt bedrijven in Zuid-Holland groeien via SEO.</p>
outro = """
<p><strong>Wil jij hoger in Google komen en meer klanten aantrekken?</strong>
FBN Marketing helpt bedrijven in Zuid-Holland met effectieve SEO en contentstrategie. Neem contact op voor een vrijblijvende scan van je online vindbaarheid.</p>
"""
html_content += outro_html

# === YOAST SEO META ===
html_content = intro + h1 + p1 + h2 + p2 + h3 + p3 + h4 + p4 + outro

# === YOAST META ===
seo_meta = {
    "yoast_title": title,
    "yoast_meta": f"{title} - SEO tips voor ondernemers in Zuid-Holland.",
    "yoast_meta": f"{title} - Praktische SEO tips voor ondernemers in Zuid-Holland.",
    "yoast_focuskw": "SEO Zuid-Holland"
}

# === POST VERSTUREN ===
# === POST AANMAKEN ===
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
    post = res.json()
    post_link = post['link']
    print("✅ Blog gepubliceerd: ", post_link)

    # === MAIL VERSTUREN ===
    msg = MIMEText(f"Er is een nieuwe blog geplaatst op FBN Design:\n\n{title}\n{post_link}")
    msg['Subject'] = "Nieuwe blog op FBN Design"
    msg['From'] = "noreply@fbndesign.nl"
    msg['To'] = notify_email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(os.environ['EMAIL_USER'], os.environ['EMAIL_PASS'])
            smtp.send_message(msg)
            print("📧 Mail verstuurd naar:", notify_email)
    except Exception as e:
        print("❌ Mail kon niet worden verstuurd:", e)
else:
    print(f"❌ Publiceren mislukt: {res.status_code}\n{res.text}")
    print(f"❌ Mislukt: {res.status_code}\n{res.text}")
