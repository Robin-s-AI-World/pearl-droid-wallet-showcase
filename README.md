# Pearl Wallet — App Showcase

Public landing page and release distribution site for **Pearl Wallet Android**.

## Live URLs

| Host | URL | Notes |
|---|---|---|
| **Netlify** | https://pearl-wallet-showcase.netlify.app | Primary — hosts all content including large download files |
| **Vercel** | https://pearl-wallet-showcase.vercel.app | Mirror — excludes `downloads/` via `.vercelignore` (100MB file limit); download URLs point to GitHub Releases |
| **GitHub Releases** | https://github.com/rebots-online/pearl-wallet-releases | Public binary hosting — signed APKs, AABs, debug symbols |

## Deployment

### Netlify (primary)
```bash
cd ~/Desktop/github/pearl-wallet-showcase
netlify deploy --dir=. --site=02dc62c8-0007-4d66-9d33-99c9b4bd5be9 --prod
```

### Vercel (mirror)
```bash
cd ~/Desktop/github/pearl-wallet-showcase
vercel deploy --prod --yes
```

### Both hosts — parity policy
Both hosts must be kept in sync. After any content change, deploy to **both** Netlify and Vercel. The `.vercelignore` file excludes `downloads/`, `*.apk`, `*.aab`, and `*.zip` from Vercel deploys (Vercel has a 100MB per-file limit). Download URLs in the release manifest point to the public GitHub Releases repo so both hosts serve identical download links.

## Release process

1. **Build**: `bash scripts/build-release.sh` in the main `pearl-wallet-android` repo
2. **Commit & push**: prefix commit message with `v{version}.{build}:` (e.g., `v1.105.3620: fix(battery): ...`)
3. **Upload to GitHub Releases**: `gh release create v{version} --repo rebots-online/pearl-wallet-releases dist/*.apk dist/*.aab dist/*.zip`
4. **Update manifest**: download URLs in `releases/current-public-release-manifest.json` must point to `https://github.com/rebots-online/pearl-wallet-releases/releases/download/v{version}/...`
5. **Copy manifests**: sync `releases/` from `www-landing-page/` to this showcase repo
6. **Deploy both**: Netlify then Vercel

## Structure

```
├── index.html              # Main landing page (manifest-driven, 91KB)
├── app-showcase-12s.html   # 12-second auto-playing showcase
├── learn.html              # Educational content
├── privacy.html            # Privacy policy
├── terms.html              # Terms of service
├── robots.txt              # SEO
├── sitemap.xml             # Sitemap
├── netlify.toml            # Netlify config (headers, caching)
├── .vercelignore           # Excludes large binaries from Vercel
├── releases/               # Release manifests (JSON + XML)
│   ├── current-public-release-manifest.json
│   ├── current-public-release-manifest.xml
│   └── release-manifest-v{version}.json
├── downloads/              # Binary artifacts (Netlify only; not in Vercel)
├── assets/                 # Media assets (audio, PDFs, images)
├── content/papers/         # Whitepapers and technical docs
├── marketing/outreach/     # Marketing materials
├── DESIGN-HANDOFF.md       # Design system handoff doc
└── DESIGN-MANIFEST.json    # Design manifest
```

## Source repos

| Repo | Visibility | Purpose |
|---|---|---|
| `rebots-online/pearl-wallet-android` | Private | Main app source code, build scripts, release manifest generation |
| `rebots-online/pearl-wallet-releases` | Public | Public release artifacts (APKs, AABs, symbols) |
| `Robin-s-AI-World/pearl-droid-wallet-showcase` | Public | This showcase repo (Vercel git-linked) |
