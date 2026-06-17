# Stevan Kojić Portfolio

Minimalističan art portfolio sajt sa GitHub Sheets + Drive integracijom.

## 🎨 Features

- **Minimalist design**: Monospace font, "notepad" aesthetic
- **3 pages**: Portfolio gallery, About (biography + CV + exhibitions), Video
- **82 high-res images**: 1920px+ originals from your Cargo.site
- **Google Sheets integration**: Edit content in Sheets, auto-sync to site
- **Google Drive storage**: All images stored and linked in Drive
- **Static HTML**: No database, no server runtime needed
- **Fast deployment**: Ready for any static host (Cloudflare Pages, GitHub Pages, your own server)

## 🚀 Quick Start

### 1. Install & Build

```bash
npm install
npm run build
```

Output: `dist/` folder (ready to deploy)

### 2. Develop Locally

```bash
npm run dev
```

Opens at `http://localhost:3000`

### 3. Edit Content

Your data is in Google Sheets:  
https://docs.google.com/spreadsheets/d/1dNQ0IC7oy__tCe4asERJ10AWUSaffU6MZWZiAWmoEkw

Edit titles, descriptions, dates directly in the sheet. Images are in Drive:  
https://drive.google.com/drive/folders/18jtSdgL4i0qHNfwo1MkiXpph-S1WrnQo

### 4. Re-sync Google Sheets

When you make changes in Google Sheet:

```bash
python3 populate_sheet.py
npm run build
```

## 📁 File Structure

```
stevankojic/
├── src/
│   ├── pages/              # Astro page components
│   │   ├── index.astro     # Gallery page
│   │   ├── about.astro     # About page
│   │   └── video.astro     # Video page
│   ├── data/
│   │   └── portfolio.json  # Extracted portfolio data
│   └── layouts/            # Page layouts (if needed)
│
├── public/
│   └── images/             # All 82 portfolio images (76 MB)
│
├── dist/                   # Built website (ready for deployment)
│   ├── index.html
│   ├── about/
│   ├── video/
│   └── images/
│
├── astro.config.mjs        # Astro configuration
├── package.json            # Dependencies
├── credentials.json        # Google OAuth credentials (git-ignored)
├── token.json              # OAuth token (auto-generated, git-ignored)
├── build-site.py           # Extract data from scrape/
├── populate_sheet.py       # Upload to Google Sheets & Drive
└── SETUP.md                # Initial setup guide
```

## 🔐 Google Integration

### OAuth Setup (First Time)

```bash
python3 populate_sheet.py
```

- Opens browser for Google login
- Uploads all images to Drive folder
- Populates Google Sheet with portfolio data
- Saves token locally for future runs

### Re-sync Anytime

```bash
python3 populate_sheet.py  # Updates Drive & Sheet
npm run build              # Rebuilds HTML from latest data
```

## 📤 Deployment Options

### Option 1: Cloudflare Pages (Recommended - Free)

```bash
# Push to GitHub first
git push origin main

# Then connect repo to Cloudflare Pages
# - Framework: Astro
# - Build command: npm run build
# - Build output: dist
```

### Option 2: GitHub Pages (Free)

```bash
npm run build
# Deploy dist/ folder to gh-pages branch
```

### Option 3: Your Own Server

```bash
# Copy dist/ folder to your web server
scp -r dist/* user@yourserver:/var/www/html/
```

For nginx/Apache, just serve the `dist/` folder as static content.

### Option 4: Vercel (Free)

```bash
npm run build
# Connect GitHub repo to Vercel dashboard
```

## 🛠️ Development

### Edit HTML/CSS

Modify `src/pages/*.astro` files to change layout and styling.

### Edit JavaScript

Keep `src/pages/*.astro` files minimal. Add JS in `<script>` tags.

### Add New Pages

Create `src/pages/page-name.astro` and it automatically becomes `/page-name/`

## 📝 Content Workflow

1. **Edit in Google Sheet** (easiest for non-developers)
2. **Run** `python3 populate_sheet.py`
3. **Build** `npm run build`
4. **Deploy** `dist/` folder

## 🔧 Commands

```bash
npm run dev      # Start dev server (http://localhost:3000)
npm run build    # Build static site to dist/
npm run preview  # Preview built site locally
```

## 📚 Resources

- **Astro docs**: https://docs.astro.build
- **Google Sheets API**: https://developers.google.com/sheets/api
- **Google Drive API**: https://developers.google.com/drive/api

## 💡 Tips

- Images are lazy-loaded for better performance
- All images are 1920px+ originals for print quality
- Gallery grid is responsive (mobile-friendly)
- Monospace font loads locally (no external fonts)

## 🗂️ Source Data

Original scrape from Cargo.site is in `scrape/` folder (git-ignored):
- `scrape/content/` — HTML, text, image manifests
- `scrape/assets/images/` — 82 original images (76 MB)

---

**Sajt je live kada je `dist/` folder na tvom serveru.**

Questions? Check SETUP.md for initial configuration.
