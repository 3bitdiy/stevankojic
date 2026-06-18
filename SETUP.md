# Setup

## Local

```bash
npm install
npm run dev
```

## GitHub Pages

One-time, in the repo on GitHub:

1. Settings → Pages → Build and deployment → Source: GitHub Actions.
2. Push to `main`. The workflow in `.github/workflows/deploy.yml` builds and deploys.

`astro.config.mjs` sets `base: '/stevankojic/'` to match the Pages subpath.

## Add a work

1. Create a Markdown file in `src/content/works/` (see README for fields).
2. Put any images in `public/images/`.
3. Commit and push.
