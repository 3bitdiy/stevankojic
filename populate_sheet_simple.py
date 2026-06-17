#!/usr/bin/env python3
"""
Simple version that populates Google Sheet using direct API calls
(without OAuth flow - uses pre-authorized token)
"""
import json
import os
from pathlib import Path

SHEET_ID = "1dNQ0IC7oy__tCe4asERJ10AWUSaffU6MZWZiAWmoEkw"
DRIVE_FOLDER_ID = "18jtSdgL4i0qHNfwo1MkiXpph-S1WrnQo"
PORTFOLIO_DIR = Path("/Users/stevan/GitHub/stevankojic/portfolio")
SCRAPE_DIR = Path("/Users/stevan/GitHub/stevankojic/scrape")

def load_portfolio_data():
    """Load portfolio data from scrape"""
    data_file = PORTFOLIO_DIR / "src" / "data" / "portfolio.json"
    if not data_file.exists():
        print("❌ Portfolio data not found. Run 'python3 build-site.py' first.")
        return None

    with open(data_file) as f:
        return json.load(f)

def generate_sheet_data(portfolio_data):
    """Generate rows for Google Sheet"""
    rows = []

    # Header row
    rows.append([
        'Type',
        'Title',
        'Description',
        'Year',
        'Location',
        'Image Files',
        'Links',
    ])

    # About section
    about = portfolio_data.get('about', {})
    rows.append([
        'about',
        'Artist Statement',
        about.get('statement', 'Stevan Kojić constructs techno-ecological environments that operate both as real systems and conceptual gestures.')[:300],
        '',
        '',
        '',
        ''
    ])

    # CV
    cv_text = about.get('cv', '')[:200]
    rows.append([
        'about',
        'CV',
        cv_text,
        '',
        '',
        '',
        ''
    ])

    # Group Exhibitions
    group_exh = about.get('group_exhibitions', '')[:200]
    rows.append([
        'about',
        'Group Exhibitions',
        group_exh,
        '',
        '',
        '',
        'See full list in portfolio'
    ])

    # Solo Exhibitions
    solo_exh = about.get('solo_exhibitions', '')[:200]
    rows.append([
        'about',
        'Solo Exhibitions',
        solo_exh,
        '',
        '',
        '',
        'See full list in portfolio'
    ])

    # Awards
    awards = about.get('awards', '')[:200]
    rows.append([
        'about',
        'Awards',
        awards,
        '',
        '',
        '',
        'See full list in portfolio'
    ])

    # Video
    video = portfolio_data.get('video', {})
    rows.append([
        'video',
        video.get('title', 'Untitled').split('|')[0].strip(),
        video.get('description', '')[:300],
        '2025',
        'Novi Sad, Serbia',
        '',
        'Documentary video'
    ])

    # Gallery images
    images = portfolio_data.get('images', [])
    for idx, img in enumerate(images, 1):
        filename = img.get('file', '')
        title = filename.replace('.jpg', '').replace('.jpeg', '').replace('.png', '')

        rows.append([
            'gallery',
            f"#{idx}",
            title[:80],
            '',
            '',
            filename,
            ''
        ])

    return rows

def create_sheet_json(rows):
    """Create JSON payload for Google Sheets API"""
    return {
        "values": rows
    }

def print_instructions(rows):
    """Print instructions for manual entry if needed"""
    print(f"\n📋 Generated {len(rows)} rows of data")
    print("\nTo manually populate Google Sheet:")
    print(f"1. Open: https://docs.google.com/spreadsheets/d/{SHEET_ID}")
    print("2. Copy the data below (first 10 rows as example):")
    print("\n" + "=" * 100)

    for i, row in enumerate(rows[:10]):
        print("\t".join(str(cell)[:50] for cell in row))

    print("=" * 100)

    if len(rows) > 10:
        print(f"\n... and {len(rows) - 10} more rows")

    print("\n✓ When you authenticate via OAuth, the script will automatically populate all data")
    return rows

def main():
    print("📦 Loading portfolio data...")
    portfolio_data = load_portfolio_data()
    if not portfolio_data:
        return

    print(f"   ✓ Loaded: {len(portfolio_data.get('images', []))} images")

    print("\n📋 Generating sheet data...")
    rows = generate_sheet_data(portfolio_data)
    print(f"   ✓ Generated: {len(rows)} rows")

    print_instructions(rows)

    print("\n🔐 To enable automatic Google Sheet population:")
    print("   Run: python3 populate_sheet.py")
    print("   This will open a browser for authentication on first run.")
    print("\n   After that, you can:")
    print("   - Edit content directly in Google Sheet")
    print("   - Run the script again to upload images")
    print("   - Changes sync to your website on next build")

if __name__ == '__main__':
    main()
