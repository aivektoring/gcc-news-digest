# GCC Hírek Gyűjtő – Telepítési Útmutató (INGYENES)

## ✅ Teljesen ingyenes megoldás

- **Fordítás:** Google Translate (ingyenes, API kulcs nélkül)
- **Szűrés:** Kulcsszó-alapú (ingyenes)
- **GitHub Actions:** Ingyenes
- **Gmail:** Ingyenes
- **Teljes költség: 0 USD/hó** 🎉

---

## Előfeltételek

- GitHub fiók
- Google/Gmail fiók

**NEM kell:** OpenAI fiók, API kulcsok

---

## 1. lépés: GitHub Repository előkészítése

### 1.1 Repository klónozása vagy létrehozása

```bash
mkdir gcc-news-digest
cd gcc-news-digest
git init
```

### 1.2 Fájlok másolása

Másolj be a repository gyökerébe:
- `news_digest.py` – a fő Python script
- `.github/workflows/news-digest.yml` – a GitHub Actions workflow
- `requirements.txt` – Python függőségek

Könyvtár szerkezet:
```
gcc-news-digest/
├── .github/
│   └── workflows/
│       └── news-digest.yml
├── news_digest.py
├── requirements.txt
└── README.md
```

### 1.3 requirements.txt

```
feedparser==6.0.10
google-translate-extended==1.3.5
```

---

## 2. lépés: Gmail SMTP beállítása

### 2.1 Google fiók – 2-faktoros hitelesítés

1. Lépj be a https://myaccount.google.com/ oldalra
2. **Security** → **2-Step Verification** – kapcsold be (ha még nincs)
3. Bizonyítsd be magad telefonnal

### 2.2 Gmail App Password létrehozása

1. Menj vissza az **Account** → **Security**
2. Görgess le az **App passwords** részhez
3. Válassz: **Mail** és **Windows Computer** (vagy általános "Other")
4. Az Google generál egy 16 karakteres jelszót – **másolj le**

Például: `abcd efgh ijkl mnop`

---

## 3. lépés: GitHub Secrets beállítása

A repository Settings-ben tárold az alábbi secret-eket:

1. **GMAIL_USER** = A Gmail cím (pl. `your-email@gmail.com`)
2. **GMAIL_APP_PASSWORD** = Az App Password (16 karakter, szóközök nélkül)
3. **RECIPIENT_EMAIL** = Kinek küldj e-mailt (pl. `sandor.laszlo@roto-frank.com`)

### Hogyan adjuk hozzá?

1. GitHub → Repository → **Settings** → **Secrets and variables** → **Actions**
2. Kattints **New repository secret**
3. Add meg a nevet és az értéket

---

## 4. lépés: Workflow aktiválása és tesztelése

### 4.1 Push to GitHub

```bash
git add .
git commit -m "Initial GCC news digest setup"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/gcc-news-digest.git
git push -u origin main
```

### 4.2 Teszt futtatás

1. GitHub → Repository → **Actions**
2. Válaszd ki a **GCC News Digest** workflow-t
3. Kattints **Run workflow** → **Run workflow**
4. Várd meg a futást (~1-2 perc)

### 4.3 Logok megtekintése

1. Az Actions oldalon kattints a futtatásra
2. Az **Logs** fülön meglátod a teljes naplót

Ha hibád akad, az itt fog megjelenni!

---

## 5. lépés: Ütemezés testreszabása (opcionális)

### Időzóna problémája

GitHub Actions UTC időt használ. Ha más időzónában szeretnéd az ütemezést:

**Budapest (UTC+1/+2 téli/nyári idő):**
- 7:30 reggel = 5:30 UTC (vagy 6:30 nyári időben)
- **Cron:** `30 5 * * *` (vagy próbáld meg `30 6 * * *`)

**Cron formátum:** `perc óra * * *`

Ha módosítani akarod, szerkeszd a `.github/workflows/news-digest.yml` fájlban:

```yaml
on:
  schedule:
    - cron: '30 5 * * *'  # 5:30 UTC = kb. 7:30 Budapest idő
```

---

## Hibakeresés

### E-mail nem érkezik

- **Ellenőrizd:** Gmail hitelességi naplóban van-e bejelentkezési kísérlet?
  - https://myaccount.google.com/security-checkup
- **App password helyes?** (szóközök nélkül)
- **Recipient email helyes?**

### Fordítás nem működik

- A Google Translate néha lassú lehet (2-3 másodperc/hír)
- Ha sok hír van, a script hosszabb ideig futhat
- A forgalmazás korlátozása miatt esetleg hibaüzenet jelenhet meg – ez normális, a script újrapróbálja

### RSS forrás nem működik

- Próbáld meg manuálisan betölteni az URL-t egy böngészőben
- Vagy fuss le helyileg `python news_digest.py` (environment variables beállítása után)

### Helyi tesztelés (előbb)

```bash
# Environment variables beállítása
export GMAIL_USER="your-email@gmail.com"
export GMAIL_APP_PASSWORD="your-app-password"
export RECIPIENT_EMAIL="sandor.laszlo@roto-frank.com"

# Script futtatása
python news_digest.py
```

---

## Tippek és optimalizáció

### 1. RSS Forrásokat módosítani

Szerkeszd a `news_digest.py` fájl **RSS_SOURCES** szótárát.

### 2. Hírnyelvezet szűrésére

A `simple_keyword_filter()` függvénybe adj hozzá további kulcsszavakat.

### 3. E-mail sablon testreszabása

A `create_email_body()` függvényt módosíthatod az HTML formázáshoz.

### 4. Hírszám módosítása

```python
MAX_ARTICLES = 10  # Maximum hány hír az e-mailben (default: 10)
```

---

## Költség-áttekintés

| Komponens | Költség |
|-----------|---------|
| Google Translate | ✅ **Ingyenes** |
| GitHub Actions | ✅ **Ingyenes** (2000 perc/hó) |
| Gmail SMTP | ✅ **Ingyenes** |
| **Teljes** | **✅ 0 USD/hó** |

---

## Kérdések/Támogatás

Ha bármilyen hiba lépne fel:
1. Ellenőrizd a GitHub Actions logokat
2. Fuss le helyileg a scriptet hibaüzenetért
3. Ellenőrizd, hogy a Gmail App Password helyes-e

---

**Sikeres beállítást kívánunk! 🚀**
