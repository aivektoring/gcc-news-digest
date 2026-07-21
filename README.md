# 📰 GCC Gazdasági Hírek Gyűjtő

Automata hírek gyűjtő rendszer, amely naponta 7:30-kor összegyűjti a GCC régió (Saudi-Arábia, UAE, Kuwait, Qatar, Bahrain, Oman) gazdasági, építőipari és politikai híreit, AI szűréssel, és magyar + német fordítással elküldi e-mailben.

## ✨ Főbb funkciókat

- **Automatikus RSS gyűjtés** – 18+ megbízható nemzetközi forrásból (Arab News, Reuters, BBC, Bloomberg, DW, stb.)
- **Kulcsszó-alapú szűrés** – A legfontosabb GCC-vel kapcsolatos hírek kiválasztása
- **Duplikáció eltávolítása** – ugyanaz a hír ne jelenjen meg többször
- **Automatikus fordítás** – Google Translate-tel magyar és német fordítás (INGYENES)
- **Professzionális e-mail** – HTML formázás, jó olvashatóság
- **Naponta 7:30-kor futás** – GitHub Actions cron job-ként
- **Teljesen ingyenes** – 0 USD/hó 🎉

## 📋 Mit tartalmaz?

```
├── news_digest.py           # Fő Python script
├── requirements.txt         # Python függőségek
├── .github/workflows/
│   └── news-digest.yml      # GitHub Actions workflow (7:30 ütemezés)
├── SETUP.md                 # Telepítési útmutató
└── README.md                # Ez a fájl
```

## 🚀 Gyors start

### 1. Repository klónozása vagy létrehozása (GitHub-on)
### 2. Fájlok másolása a repository-ba
### 3. Gmail App Password létrehozása (ingyenes)
### 4. GitHub Secrets beállítása (csak Gmail adatok)
### 5. Workflow aktiválása

**Részletesen lásd: SETUP_FREE.md**

## 🌍 RSS Forrásak

Alapértelmezés szerint az alábbi forrásokból gyűjt:

**Közel-keleti angol:**
- Arab News, Arabian Business, Khaleej Times, The National UAE, Zawya, Maaal

**Nemzetközi:**
- Reuters, AP News, BBC, Financial Times, The Guardian, CNBC, CNN

**Speciális:**
- DW (német), TRT World (török), Anadolu Agency, Xinhua (kínai)

Könnyen módosítható a `news_digest.py` fájlban a `RSS_SOURCES` szótár.

## 📧 E-mail formátuma

Minden reggel egy e-mail érkezik:

```
📰 GCC Hírek – 2024. július 21.

🇭🇺 MAGYAR VERZIÓ
1. [Hír cím magyarul]
   Forrás: Arab News | 2024-07-21
   [Összefoglaló az angol cikkből lefordítva]
   📖 Teljes cikk →

...további hírek...

🇩🇪 DEUTSCHE VERSION
1. [Hír cím németül]
   Quelle: Arab News | 2024-07-21
   [Zusammenfassung übersetzt]
   📖 Vollständigen Artikel →

...weitere Nachrichten...
```

## ⚙️ Konfigurációk

### Ütemezés módosítása

`.github/workflows/news-digest.yml` fájlban:
```yaml
cron: '30 5 * * *'  # 5:30 UTC = kb. 7:30 Budapest idő
```

### Híranyagok száma

`news_digest.py` fájlban:
```python
MAX_ARTICLES = 10  # Maximum 10 hír/e-mail
```

### Keresési időtartam

```python
HOURS_BACK = 24  # Csak az utolsó 24 óra hírei
```

### E-mail stílus

Szerkeszd a `create_email_body()` függvényt az HTML/CSS módosításához.

## 💰 Költségek

| Eszköz | Költség |
|--------|---------|
| Google Translate | ✅ Ingyenes |
| GitHub Actions | ✅ Ingyenes (2000 perc/hó) |
| Gmail SMTP | ✅ Ingyenes |
| **Összesen** | **✅ 0 USD/hó** |

## 🐛 Hibakeresés

### Workflow nem futott el
1. Ellenőrizd, hogy a `.github/workflows/news-digest.yml` a helyén van-e
2. GitHub → Actions → Workflow logok

### E-mail nem érkezik
1. Ellenőrizd a GitHub Secrets helyességét
2. Gmail hitelesítési napló: https://myaccount.google.com/security-checkup
3. Lokal tesztelés: `python news_digest.py`

### OpenAI hiba
1. Ellenőrizd az API kulcsot
2. Van-e kredit az OpenAI fiókodban?
3. Usage napló: https://platform.openai.com/account/usage

## 🔒 Biztonság

- **Secrets nem jelentek meg** a GitHub Actions logokban
- **Gmail App Password** – csak az SMTP-hez, nem a teljes Google fiók
- **Local teszt:** az environment variables nem tárolódnak le

## 📚 További módosítások

### RSS forrás hozzáadása

```python
RSS_SOURCES = {
    "New Source": "https://example.com/rss",
    # ... más források
}
```

### Fordítási nyelvek módosítása

`create_email_body()` függvényben módosítsd a `translate_text()` hívásokat.

### AI szűrés finomítása

Módosítsd a `filter_articles_with_ai()` függvényt a system prompt-ban.

## 📖 Dokumentáció

- **Feedparser:** https://feedparser.readthedocs.io/
- **Google Translate Extended:** https://github.com/nidhaloff/google-translate-extended
- **Gmail SMTP:** https://support.google.com/mail/answer/7104828

## 📞 Támogatás

Kérdések vagy problémák? Ellenőrizd:
1. **SETUP_FREE.md** – telepítési útmutató (ingyenes verzió)
2. GitHub Actions logok (Actions fülön)
3. Helyi Python scriptet (`python news_digest.py`)

## 📝 Licenc

MIT License – szabad felhasználás, módosítás, terjesztés.

---

**Sikeres beállítást kívánunk! 🚀**

Készítette: Claude AI | 2024. július
