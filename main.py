import requests
import base64
import os
from datetime import datetime

# Gegevens uit GitHub Secrets
wp_url = os.environ['WP_URL']
wp_user = os.environ['WP_USER']
wp_password = os.environ['WP_APP_PASSWORD']
email_notify = os.environ['EMAIL_NOTIFY']

# Bloginhoud
title = f"Waarom SEO belangrijk is voor B2B – {datetime.now().strftime('%Y-%m-%d')}"
content = """
<p><strong>SEO is essentieel in 2025.</strong> Bedrijven die online zichtbaar zijn, hebben voorsprong. In dit artikel lees je waarom content en optimalisatie jouw groei versnellen.</p>
"""

# Auth
token = base64.b64encode(f"{wp_user}:{wp_password}".encode()).decode("utf-8")
headers = {
    "Authorization": f"Basic {token}",
    "Content-Type": "application/json"
}

# WordPress POST verzoek
data = {
    "title": title,
    "content": content,
    "status": "publish"
}

r = requests.post(f"{wp_url}/wp-json/wp/v2/posts", headers=headers, json=data)

if r.status_code == 201:
    print("✅ Blog geplaatst!")
else:
    print(f"❌ Mislukt met status {r.status_code}")
    print(r.text)
