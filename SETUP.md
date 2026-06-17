# Portfolio Setup - Google Sheets Integration

## Quick Start (Recommended)

Your portfolio website is ready! Now we'll set up Google Sheets for easy content management.

### Step 1: Authenticate with Google

Open your terminal and run:

```bash
cd /Users/stevan/GitHub/stevankojic/portfolio
python3 populate_sheet.py
```

This will:
1. **Open a browser** with Google login
2. Click your email (`stevankojic.com@gmail.com`)
3. Click "Continue" to authorize access
4. Close the browser - the script will continue automatically

### What Happens Next

The script will automatically:
- ✓ Upload all 82 images to Google Drive folder
- ✓ Populate Google Sheet with all portfolio data
- ✓ Create token.json (saved locally, used for future runs)

**Time:** ~5-10 minutes (due to image upload size: 76 MB)

### After Setup

**Your Google Sheet:**
```
https://docs.google.com/spreadsheets/d/1dNQ0IC7oy__tCe4asERJ10AWUSaffU6MZWZiAWmoEkw
```

**Your Drive Folder:**
```
https://drive.google.com/drive/folders/18jtSdgL4i0qHNfwo1MkiXpph-S1WrnQo
```

## Updating Content

Now when you want to change content:

1. **Edit in Google Sheet** directly (titles, descriptions, dates, etc.)
2. **Run build to generate HTML:**
   ```bash
   npm run build
   ```
3. **Deploy the `dist/` folder** to your server

## File Structure

```
portfolio/
├── dist/                 # Built website (ready for deployment)
│   ├── index.html       # Gallery page
│   ├── about/index.html # About page
│   ├── video/index.html # Video page
│   └── images/          # All 82 portfolio images
│
├── src/
│   ├── pages/           # Astro page templates
│   ├── data/            # Portfolio data (generated)
│   └── layouts/
│
├── credentials.json     # Google OAuth credentials
├── token.json          # Auto-generated auth token (git ignored)
├── populate_sheet.py   # Script to sync with Google Sheets
└── astro.config.mjs    # Astro configuration
```

## Troubleshooting

**"Port already in use" error:**
The OAuth server picks an available port automatically. If you see "Please visit" in terminal, follow that URL.

**Google Sheet not populating:**
Check that your OAuth token is valid. Delete `token.json` and run script again.

**Images not uploading:**
Check your internet connection. Script resumes from where it left off.

## Next: Deploy to Your Server

When ready to go live:

```bash
# Build final version
npm run build

# Deploy contents of dist/ folder to your server
# Via FTP, SSH, or cloud platform (see main README)
```

---

✅ Setup is complete! Run `python3 populate_sheet.py` to finalize.
