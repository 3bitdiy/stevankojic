#!/usr/bin/env python3
"""Build portfolio site by extracting data from scrape"""
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

SCRAPE = Path("/Users/stevan/GitHub/stevankojic/scrape")

def extract_text_between(text, start, end):
    """Extract text between two strings"""
    m = re.search(f"{re.escape(start)}(.+?){re.escape(end)}", text, re.DOTALL)
    return m.group(1).strip() if m else ""

def parse_about():
    """Parse about.text.txt"""
    about_file = SCRAPE / "content" / "about.text.txt"
    if not about_file.exists():
        return {}

    text = about_file.read_text()
    lines = text.split('\n')

    # Artist statement je prvi paragraf
    statement = extract_text_between(text, "artist statement\n\n", "\n\n\n")

    # CV data
    cv = extract_text_between(text, "cv\n\n", "\n\ngroup exhibitions")

    # Group exhibitions
    group_exhibitions = extract_text_between(text, "group exhibitions", "\n\n\nsolo exhibitions")

    # Solo exhibitions
    solo_exhibitions = extract_text_between(text, "solo exhibitions", "\n\nawards")

    # Awards
    awards = extract_text_between(text, "awards", "\n\n\ncontact")

    return {
        'statement': statement,
        'cv': cv,
        'group_exhibitions': group_exhibitions,
        'solo_exhibitions': solo_exhibitions,
        'awards': awards,
    }

def parse_video():
    """Parse video.text.txt"""
    video_file = SCRAPE / "content" / "video.text.txt"
    if not video_file.exists():
        return {}

    text = video_file.read_text()
    lines = [l.strip() for l in text.split('\n') if l.strip()]

    # Title je drugi red
    title = lines[1] if len(lines) > 1 else "Untitled"

    # Description počinje nakon naslova
    desc_start = text.find(title) + len(title)
    desc = text[desc_start:].strip()

    return {
        'title': title,
        'description': desc,
    }

def parse_projects():
    """Parse index.html za projekte"""
    index_html = SCRAPE / "content" / "index.html"
    if not index_html.exists():
        return []

    with open(index_html) as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Pronađi sve script tagove koji sadrže JSON
    projects = []
    scripts = soup.find_all('script', type='application/json')

    for script in scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, list):
                projects.extend(data)
            elif isinstance(data, dict):
                projects.append(data)
        except:
            pass

    return projects[:20]  # Limit za sada

def get_images():
    """Get image manifest"""
    manifest_file = SCRAPE / "content" / "images_manifest.json"
    if manifest_file.exists():
        return json.loads(manifest_file.read_text())
    return []

def main():
    print("📖 Extracting portfolio data...")

    about = parse_about()
    video = parse_video()
    projects = parse_projects()
    images = get_images()

    data = {
        'about': about,
        'video': video,
        'projects': projects,
        'images': images,
    }

    # Save as JSON for Astro
    out_file = Path("src/data/portfolio.json")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    print(f"✓ About: {len(about)} sections")
    print(f"✓ Video: {video.get('title', 'N/A')}")
    print(f"✓ Projects: {len(projects)}")
    print(f"✓ Images: {len(images)}")
    print(f"\n✅ Saved to src/data/portfolio.json")

if __name__ == '__main__':
    main()
