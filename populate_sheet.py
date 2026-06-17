#!/usr/bin/env python3
"""
Populates Google Sheet with portfolio data and uploads images to Drive
"""
import json
import os
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file'
]

SHEET_ID = "1dNQ0IC7oy__tCe4asERJ10AWUSaffU6MZWZiAWmoEkw"
DRIVE_FOLDER_ID = "18jtSdgL4i0qHNfwo1MkiXpph-S1WrnQo"
PORTFOLIO_DIR = Path("/Users/stevan/GitHub/stevankojic/portfolio")
SCRAPE_DIR = Path("/Users/stevan/GitHub/stevankojic/scrape")

def get_authenticated_services():
    """Authenticate with Google APIs using OAuth"""
    creds = None
    token_file = PORTFOLIO_DIR / "token.json"

    # Load existing token if available
    if token_file.exists():
        import pickle
        try:
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        except:
            creds = None

    # If no valid credentials, create new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(PORTFOLIO_DIR / 'credentials.json'),
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save token for future use
        import pickle
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

    sheets_service = build('sheets', 'v4', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)
    return sheets_service, drive_service, creds

def upload_images_to_drive(drive_service):
    """Upload all images from scrape/assets/images to Drive folder"""
    image_dir = SCRAPE_DIR / "assets" / "images"
    uploaded = {}

    if not image_dir.exists():
        print(f"❌ Image directory not found: {image_dir}")
        return uploaded

    image_files = sorted(image_dir.glob("*"))
    total = len(image_files)

    for idx, image_file in enumerate(image_files, 1):
        if image_file.is_file() and image_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
            try:
                file_metadata = {
                    'name': image_file.name,
                    'parents': [DRIVE_FOLDER_ID]
                }
                media = MediaFileUpload(str(image_file), mimetype='image/*')
                result = drive_service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id,webViewLink'
                ).execute()

                uploaded[image_file.name] = result.get('id')
                print(f"  [{idx}/{total}] ✓ {image_file.name}")
            except Exception as e:
                print(f"  [{idx}/{total}] ✗ {image_file.name}: {e}")

    return uploaded

def load_portfolio_data():
    """Load portfolio data from scrape"""
    data_file = PORTFOLIO_DIR / "src" / "data" / "portfolio.json"
    if not data_file.exists():
        print("❌ Portfolio data not found. Run 'python3 build-site.py' first.")
        return None

    with open(data_file) as f:
        return json.load(f)

def populate_sheet(sheets_service, portfolio_data, uploaded_images):
    """Populate Google Sheet with portfolio data"""

    rows = []

    # Header row
    rows.append([
        'Type',
        'Title',
        'Description',
        'Year',
        'Location',
        'Image Files',
        'Image Drive IDs',
    ])

    # About section
    about = portfolio_data.get('about', {})
    rows.append([
        'about',
        'Artist Statement',
        about.get('statement', '')[:500],
        '',
        '',
        '',
        ''
    ])

    # CV
    rows.append([
        'about',
        'CV',
        about.get('cv', '')[:500],
        '',
        '',
        '',
        ''
    ])

    # Group Exhibitions
    rows.append([
        'about',
        'Group Exhibitions',
        about.get('group_exhibitions', '')[:500],
        '',
        '',
        '',
        ''
    ])

    # Solo Exhibitions
    rows.append([
        'about',
        'Solo Exhibitions',
        about.get('solo_exhibitions', '')[:500],
        '',
        '',
        '',
        ''
    ])

    # Awards
    rows.append([
        'about',
        'Awards',
        about.get('awards', '')[:500],
        '',
        '',
        '',
        ''
    ])

    # Video
    video = portfolio_data.get('video', {})
    rows.append([
        'video',
        video.get('title', 'Untitled'),
        video.get('description', '')[:500],
        '2025',
        'Novi Sad',
        '',
        ''
    ])

    # Gallery images
    images = portfolio_data.get('images', [])
    for idx, img in enumerate(images, 1):
        filename = img.get('file', '')
        drive_id = uploaded_images.get(filename, '')

        rows.append([
            'gallery',
            f"Image {idx}",
            filename.replace('.jpg', '').replace('.jpeg', '').replace('.png', '')[:100],
            '',
            '',
            filename,
            drive_id
        ])

    # Update sheet
    body = {
        'values': rows
    }

    try:
        result = sheets_service.spreadsheets().values().update(
            spreadsheetId=SHEET_ID,
            range='Sheet1!A1',
            valueInputOption='RAW',
            body=body
        ).execute()

        print(f"\n✓ Updated {result.get('updatedRows')} rows in Google Sheet")
        print(f"   Total rows: {len(rows)}")
        return True
    except Exception as e:
        print(f"❌ Failed to update sheet: {e}")
        return False

def main():
    print("🔐 Authenticating with Google APIs...")
    try:
        sheets_service, drive_service, creds = get_authenticated_services()
        print("   ✓ Authenticated")
    except Exception as e:
        print(f"   ❌ Authentication failed: {e}")
        return

    print("\n📦 Loading portfolio data...")
    portfolio_data = load_portfolio_data()
    if not portfolio_data:
        return

    print(f"   ✓ Loaded data: {len(portfolio_data.get('images', []))} images")

    print("\n📸 Uploading images to Google Drive...")
    print(f"   Folder: https://drive.google.com/drive/folders/{DRIVE_FOLDER_ID}")
    uploaded_images = upload_images_to_drive(drive_service)
    print(f"\n   ✓ Uploaded {len(uploaded_images)} images")

    print("\n📋 Populating Google Sheet...")
    print(f"   Sheet: https://docs.google.com/spreadsheets/d/{SHEET_ID}")
    if populate_sheet(sheets_service, portfolio_data, uploaded_images):
        print("\n✅ Done! Your portfolio is now in Google Sheets and Drive.")
        print("\nNext steps:")
        print("1. Open the Google Sheet to review/edit data")
        print("2. Modify any content directly in the sheet")
        print("3. When ready, the build script will fetch data from the sheet")
    else:
        print("\n❌ Failed to populate sheet")

if __name__ == '__main__':
    main()
