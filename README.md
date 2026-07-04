# Pearl Wallet — App Showcase

Public landing page and release distribution site for **Pearl Wallet Android**.

## Live URLs

| Host | URL | Notes |
|---|---|---|
| **Netlify** | https://pearl-wallet-showcase.netlify.app | Primary (promoted) |
| **GitHub Releases** | https://github.com/rebots-online/pearl-wallet-releases | Public binary hosting — signed APKs only |

## Deployment

### Netlify (primary)
```bash
cd ~/Desktop/github/pearl-wallet-showcase
netlify deploy --dir=. --site=02dc62c8-0007-4d66-9d33-99c9b4bd5be9 --prod
```

## Release process (manual local builds)

Two-step pipeline, both scripts in `scripts/`:

### Step 1 — Publish APK to GitHub Releases
```bash
./scripts/publish-release-to-github.sh <version> [path-to-dist]
# Example: ./scripts/publish-release-to-github.sh 1.124.08366
```
Uploads the signed APK only (no AAB, no debug symbols — per release policy). Uses `RELEASE_NOTES-v{version}.md` from dist if available, otherwise prompts for notes.

### Step 2 — Update showcase site
```bash
./scripts/update-pearl-showcase-release.sh <version>
# Example: ./scripts/update-pearl-showcase-release.sh 1.124.08366
```
Downloads the APK from the new GitHub release, computes SHA-256/size, regenerates `releases/current-public-release-manifest.json`, and deploys to Netlify.

### Full one-liner
```bash
VERSION=1.124.08366 && \
  ./scripts/publish-release-to-github.sh $VERSION && \
  ./scripts/update-pearl-showcase-release.sh $VERSION
```

### Commit convention
Prefix commit messages with `v{version}:` (e.g., `v1.124.08366: release — balance-display fix`).

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
├── netlify/functions/      # Netlify serverless functions
│   └── log-acceptance.js   # Clickwrap acceptance logger
├── api/                    # Vercel serverless functions
│   └── log-acceptance.js   # Clickwrap acceptance logger
├── releases/               # Release manifests (JSON + XML)
│   ├── current-public-release-manifest.json
│   ├── current-public-release-manifest.xml
│   └── release-manifest-v{version}.json
├── assets/                 # Media assets (images, PDFs)
├── scripts/                # Release automation
│   ├── publish-release-to-github.sh   # Step 1: upload APK to GitHub Releases
│   └── update-pearl-showcase-release.sh # Step 2: update manifest + deploy Netlify
├── content/papers/         # Whitepapers and technical docs
├── marketing/outreach/     # Marketing materials
├── DESIGN-HANDOFF.md       # Design system handoff doc
└── DESIGN-MANIFEST.json    # Design manifest
```

## Clickwrap Logging

The download flow includes a terms acceptance modal. When a user accepts the terms and clicks Download, a fire-and-forget beacon POSTs to `/api/log-acceptance` with the app version and accepted flag. The serverless function records:

- Timestamp (ISO 8601)
- IP address (from `x-forwarded-for` or platform headers)
- Country/region (from Vercel geo headers or Cloudflare `cf-ipcountry`)
- User-Agent
- App version
- Accepted: true

### Viewing logs

- **Netlify:** Dashboard → Functions → `log-acceptance` → Logs
- **Vercel:** Dashboard → Project → Logs (filter for `[clickwrap-acceptance]`)

### TODO: StackCP MySQL persistence

The serverless functions currently log to platform console only. When the StackCP MySQL database is provisioned, uncomment the MySQL block in both function files and set these environment variables on Netlify and Vercel:

| Variable | Description |
|---|---|
| `MYSQL_HOST` | StackCP MySQL server hostname |
| `MYSQL_PORT` | MySQL port (default 3306) |
| `MYSQL_USER` | Database user |
| `MYSQL_PASSWORD` | Database password |
| `MYSQL_DATABASE` | Database name |

**StackCP setup:**
1. Log into StackCP → MySQL Databases → Create a new database and user
2. Enable remote MySQL access (add `%` as allowed host, or restrict to Netlify/Vercel egress IPs)
3. Run the schema SQL below via phpMyAdmin or StackCP's database tool
4. Set the environment variables on Netlify and Vercel
5. Install `mysql2` as a dependency: `npm install mysql2`
6. Uncomment the MySQL block in `netlify/functions/log-acceptance.js` and `api/log-acceptance.js`
7. Redeploy both hosts

**Schema:**
```sql
CREATE TABLE clickwrap_acceptances (
  id INT AUTO_INCREMENT PRIMARY KEY,
  accepted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  ip_address VARCHAR(45),
  country VARCHAR(2),
  region VARCHAR(100),
  user_agent TEXT,
  app_version VARCHAR(50),
  accepted BOOLEAN DEFAULT TRUE
);
```

## Source repos

| Repo | Visibility | Purpose |
|---|---|---|
| `rebots-online/pearl-wallet-android` | Private | Main app source code, build scripts, release manifest generation |
| `rebots-online/pearl-wallet-releases` | Public | Public release artifacts (signed APKs only) |
| `Robin-s-AI-World/pearl-droid-wallet-showcase` | Public | This showcase repo (Vercel git-linked) |
