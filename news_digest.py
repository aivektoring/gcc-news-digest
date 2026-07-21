#!/usr/bin/env python3
"""
GCC Gazdasági Hírek Gyűjtő és Email Küldő
Naponta 7:30-kor fut (GitHub Actions cron)
"""

import os
import sys
import smtplib
import hashlib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
from urllib.parse import urljoin

import feedparser
from googletrans import Translator

# ============================================================================
# Konfigurációk
# ============================================================================

RSS_SOURCES = {
    "Arab News": "https://www.arabnews.com/feed",
    "Arabian Business": "https://www.arabianbusiness.com/feed",
    "Khaleej Times": "https://www.khaleejtimes.com/rss",
    "The National UAE": "https://www.thenational.ae/feed",
    "Zawya": "https://www.zawya.com/feed",
    "Reuters Business": "https://feeds.reuters.com/reuters/businessNews",
    "Reuters World": "https://feeds.reuters.com/reuters/worldNews",
    "AP News Business": "https://apnews.com/hub/business/feed",
    "BBC Business": "https://feeds.bbc.co.uk/news/business/rss.xml",
    "BBC Middle East": "https://feeds.bbc.co.uk/news/world/middle_east/rss.xml",
    "Financial Times": "https://feeds.ft.com/world",
    "The Guardian": "https://www.theguardian.com/world/rss",
    "CNBC": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "DW English": "https://www.dw.com/en/rss/feed",
    "CNN World": "http://rss.cnn.com/rss/cnn_world.rss",
    "TRT World": "https://www.trtworld.com/",
    "Anadolu Agency": "https://www.aa.com.tr/en/rss.xml",
    "Xinhua": "http://xinhuanet.com/english/rss.xml"
}

HOURS_BACK = 24  # Csak az utolsó 24 óra hírei
MAX_ARTICLES = 10  # Maximum hány hír az e-mailben

# Environment variables
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "sandor.laszlo@roto-frank.com")

# Google Translate inicializálása (ingyenes, API kulcs nélkül)
translator = Translator()

# ============================================================================
# Segéd függvények
# ============================================================================

def get_article_hash(title: str, link: str) -> str:
    """Duplikáció detektáláshoz hash készítése."""
    content = f"{title}|{link}".lower()
    return hashlib.md5(content.encode()).hexdigest()

def parse_rss_feeds() -> List[Dict]:
    """RSS forrásokból letölteni az utolsó 24 óra híreit."""
    articles = []
    cutoff_time = datetime.utcnow() - timedelta(hours=HOURS_BACK)
    seen_hashes = set()

    for source_name, rss_url in RSS_SOURCES.items():
        try:
            print(f"[RSS] {source_name} letöltése...", file=sys.stderr)
            feed = feedparser.parse(rss_url, timeout=10)

            if feed.bozo:
                print(f"[WARN] {source_name} RSS hiba: {feed.bozo_exception}", file=sys.stderr)

            for entry in feed.entries[:20]:  # Max 20 per source
                try:
                    # Közzétételi idő keresése
                    pub_date = None
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        pub_date = datetime(*entry.published_parsed[:6])
                    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                        pub_date = datetime(*entry.updated_parsed[:6])

                    # Ha nem értelmezhető az idő, kihagyni
                    if not pub_date or pub_date < cutoff_time:
                        continue

                    # Deduplikáció
                    article_hash = get_article_hash(entry.get('title', ''), entry.get('link', ''))
                    if article_hash in seen_hashes:
                        continue
                    seen_hashes.add(article_hash)

                    articles.append({
                        "title": entry.get('title', 'No title'),
                        "link": entry.get('link', ''),
                        "summary": entry.get('summary', '')[:300],
                        "source": source_name,
                        "published": pub_date.isoformat(),
                        "hash": article_hash
                    })
                except Exception as e:
                    print(f"[WARN] Hiba feldolgozáskor: {e}", file=sys.stderr)
                    continue

        except Exception as e:
            print(f"[ERROR] {source_name} letöltési hiba: {e}", file=sys.stderr)
            continue

    print(f"[OK] {len(articles)} hír letöltve (duplikáció után)", file=sys.stderr)
    return articles

def filter_articles(articles: List[Dict]) -> List[Dict]:
    """Kulcsszó-alapú szűrés a GCC-vel kapcsolatos híreket szűrni."""
    if not articles:
        return []

    print("[FILTER] Kulcsszó-alapú szűrés...", file=sys.stderr)
    return simple_keyword_filter(articles)

def simple_keyword_filter(articles: List[Dict]) -> List[Dict]:
    """Egyszerű kulcsszó-alapú szűrés, ha nincs AI."""
    keywords = [
        'gcc', 'saudi', 'uae', 'dubai', 'riyadh', 'economic', 'construction',
        'trade', 'investment', 'business', 'finance', 'arab', 'middle east',
        'oil', 'gas', 'energy', 'infrastructure', 'project', 'export', 'import',
        'politics', 'government', 'policy', 'agreement', 'deal'
    ]

    filtered = []
    for article in articles:
        text = f"{article['title']} {article['summary']}".lower()
        if any(kw in text for kw in keywords):
            filtered.append(article)
            if len(filtered) >= MAX_ARTICLES:
                break

    return filtered or articles[:MAX_ARTICLES]

def translate_text(text: str, target_language: str) -> str:
    """Szöveg fordítása Google Translate-tel (ingyenes)."""
    if not text or len(text.strip()) == 0:
        return text

    try:
        result = translator.translate(text, src_language='en', dest_language=target_language)
        return result['text'] if isinstance(result, dict) else str(result)
    except Exception as e:
        print(f"[WARN] Fordítási hiba ({target_language}): {e}", file=sys.stderr)
        return text

def create_email_body(articles: List[Dict]) -> str:
    """HTML e-mail sablon készítése."""

    # Magyar verziót
    hungarian_html = "<h2 style='color: #1a5490; border-bottom: 2px solid #1a5490; padding-bottom: 10px;'>🇭🇺 MAGYAR VERZIÓ</h2>\n"

    for i, article in enumerate(articles, 1):
        title_hu = translate_text(article['title'], 'hu')
        summary_hu = translate_text(article['summary'], 'hu')

        hungarian_html += f"""
<div style='margin-bottom: 25px; padding: 15px; background: #f9f9f9; border-left: 4px solid #1a5490;'>
    <h3 style='margin-top: 0; color: #1a5490;'>{i}. {title_hu}</h3>
    <p style='margin: 10px 0; color: #666;'><strong>Forrás:</strong> {article['source']} | {article['published'][:10]}</p>
    <p style='margin: 10px 0; line-height: 1.6;'>{summary_hu}</p>
    <p style='margin: 10px 0;'><a href='{article['link']}' style='color: #1a5490; text-decoration: none;'>📖 Teljes cikk →</a></p>
</div>
"""

    # Német verzió
    german_html = "<h2 style='color: #1a5490; border-bottom: 2px solid #1a5490; padding-bottom: 10px; margin-top: 40px;'>🇩🇪 DEUTSCHE VERSION</h2>\n"

    for i, article in enumerate(articles, 1):
        title_de = translate_text(article['title'], 'de')
        summary_de = translate_text(article['summary'], 'de')

        german_html += f"""
<div style='margin-bottom: 25px; padding: 15px; background: #f9f9f9; border-left: 4px solid #1a5490;'>
    <h3 style='margin-top: 0; color: #1a5490;'>{i}. {title_de}</h3>
    <p style='margin: 10px 0; color: #666;'><strong>Quelle:</strong> {article['source']} | {article['published'][:10]}</p>
    <p style='margin: 10px 0; line-height: 1.6;'>{summary_de}</p>
    <p style='margin: 10px 0;'><a href='{article['link']}' style='color: #1a5490; text-decoration: none;'>📖 Vollständigen Artikel →</a></p>
</div>
"""

    html = f"""
<html>
<head>
    <meta charset='utf-8'>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #1a5490, #2a6fb1); color: white; padding: 20px; border-radius: 5px; text-align: center; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #ccc; font-size: 12px; color: #666; text-align: center; }}
    </style>
</head>
<body>
    <div class='container'>
        <div class='header'>
            <h1>📰 GCC Gazdasági Hírek Napló</h1>
            <p>{datetime.now().strftime('%Y. %B %d. – %A')}</p>
        </div>

        {hungarian_html}
        {german_html}

        <div class='footer'>
            <p>Ezt az e-mailt automatikusan generálta a GCC News Digest rendszer.</p>
            <p>Kérdések vagy visszajelzés: <strong>ai.vektoring@gmail.com</strong></p>
        </div>
    </div>
</body>
</html>
"""
    return html

def send_email(subject: str, html_body: str) -> bool:
    """E-mail küldése Gmail SMTP-n keresztül."""
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        print("[ERROR] Gmail hitelesítés nincsen konfigurálva", file=sys.stderr)
        return False

    try:
        print(f"[EMAIL] E-mail küldése: {RECIPIENT_EMAIL}", file=sys.stderr)

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = GMAIL_USER
        msg['To'] = RECIPIENT_EMAIL

        # HTML rész
        part = MIMEText(html_body, 'html', 'utf-8')
        msg.attach(part)

        # Gmail SMTP
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, RECIPIENT_EMAIL, msg.as_string())

        print("[OK] E-mail sikeresen elküldve", file=sys.stderr)
        return True

    except Exception as e:
        print(f"[ERROR] E-mail küldési hiba: {e}", file=sys.stderr)
        return False

# ============================================================================
# Main
# ============================================================================

def main():
    print(f"[START] GCC News Digest ({datetime.now().isoformat()})", file=sys.stderr)

    # 1. RSS letöltés
    articles = parse_rss_feeds()
    if not articles:
        print("[ERROR] Nincsenek cikkek letöltve", file=sys.stderr)
        return False

    # 2. Szűrés (kulcsszó-alapú)
    filtered = filter_articles(articles)
    if not filtered:
        print("[ERROR] Szűrés után nincsenek cikkek", file=sys.stderr)
        return False

    # 3. E-mail előállítása
    html_body = create_email_body(filtered[:MAX_ARTICLES])

    # 4. E-mail küldése
    subject = f"📰 GCC Hírek – {datetime.now().strftime('%Y. %B %d.')}"
    send_email(subject, html_body)

    print(f"[END] Sikeres befejezés", file=sys.stderr)
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
