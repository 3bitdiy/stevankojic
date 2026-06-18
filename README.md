# Stevan Kojić Portfolio

Static portfolio site built with Astro and deployed to GitHub Pages.

Live: https://3bitdiy.github.io/stevankojic/

## Commands

```bash
npm install      # install dependencies
npm run dev      # local dev server
npm run build    # build static site to dist/
npm run preview  # preview the build
```

## Content

Each work is a Markdown file in `src/content/works/`. Works are sorted by `date` (newest first); `date` is only a sort key, `year` is the label shown.

```markdown
---
title: "Work title"
medium: "video, sound, 1:16"
venue: "Gallery / Museum name"
location: "City, Country"
year: "2025"
date: 2026-01-08
link: "example.org"
video: "YouTubeID"
images:
  - filename-01.jpg
---

Optional description text.
```

All fields except `title` and `date` are optional. Images go in `public/images/`.

The About page reads from `src/data/portfolio.json`.

## Deploy

Push to `main`. GitHub Actions (`.github/workflows/deploy.yml`) builds and deploys to GitHub Pages automatically.

## Structure

```
src/
  content/works/   # one Markdown file per work
  data/            # About-page data
  layouts/         # shared layout
  pages/           # index.astro, about.astro
public/images/     # work images
```
