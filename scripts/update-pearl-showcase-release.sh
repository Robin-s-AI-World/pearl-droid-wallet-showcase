#!/usr/bin/env bash
# update-release-and-deploy.sh
# Update the showcase release manifest with the latest public APK, then deploy to Netlify and Vercel.
# Intended to be called from the wallet build/release agent after publishing a GitHub release.
#
# Usage:
#   ./scripts/update-release-and-deploy.sh [VERSION]
#
# If VERSION is omitted, the script fetches the latest release tag from the public releases repo.
#
# Example:
#   ./scripts/update-release-and-deploy.sh v1.116.08418

set -euo pipefail

REPO="rebots-online/pearl-wallet-releases"
MANIFEST="releases/current-public-release-manifest.json"
WORK_DIR="$(mktemp -d)"

# Optional: override from command line
VERSION_ARG="${1:-}"

# Detect version
if [[ -n "$VERSION_ARG" ]]; then
  VERSION="${VERSION_ARG#v}"
else
  echo "Detecting latest release from ${REPO}..."
  LATEST_TAG="$(gh release view --repo "$REPO" --json tagName --jq '.tagName')"
  VERSION="${LATEST_TAG#v}"
fi

echo "Updating showcase for release v${VERSION}..."

APK_FILENAME="pearl-wallet-android-v${VERSION}-release-signed.apk"
APK_URL="https://github.com/${REPO}/releases/download/v${VERSION}/${APK_FILENAME}"

# Download APK
gh release download "v${VERSION}" --repo "$REPO" --pattern "${APK_FILENAME}" --dir "$WORK_DIR"

# Compute SHA-256
APK_HASH="$(sha256sum "${WORK_DIR}/${APK_FILENAME}" | awk '{print $1}')"
APK_SIZE="$(stat -c %s "${WORK_DIR}/${APK_FILENAME}")"

# Get release notes
RELEASE_BODY="$(gh release view "v${VERSION}" --repo "$REPO" --json body --jq '.body' || true)"

# Build changelog notes array from release body (each line becomes a note)
CHANGELOG_NOTES=""
while IFS= read -r line; do
  [[ -n "$line" ]] && CHANGELOG_NOTES+="\n          \"$line\","
done <<< "$RELEASE_BODY"

# Build built_at timestamp (use release publish time, or now)
BUILT_AT="$(gh release view "v${VERSION}" --repo "$REPO" --json publishedAt --jq '.publishedAt' 2>/dev/null || date -u +%Y-%m-%dT%H:%M:%SZ)"
CONTENT_DATE="$(date -u +%Y-%m-%d)"

# Source commit: use the latest commit of the main android repo at build time
SOURCE_COMMIT="$(gh api repos/Robin-s-AI-World/pearl-wallet-android/commits/master --jq '.sha' 2>/dev/null || echo 'unknown')"

# Write manifest
cat > "$MANIFEST" <<EOF
{
  "schema": "mba.robin.release-manifest.v1",
  "project": "PRL Wallet",
  "version": "${VERSION}",
  "build": "${VERSION##*.}",
  "built_at": "${BUILT_AT}",
  "content_updated_at": "${CONTENT_DATE}",
  "release_status": "tester",
  "working_status": "not-yet-first-confirmed-working-wallet",
  "public_channel_label": "Tester APK",
  "testing_warning": "This build is published so the website, release manifest, downloads, checksums, and Android install path can be tested. It is not yet confirmed as the first fully working wallet release. Do not use it for meaningful funds.",
  "copy": {
    "eyebrow": "Direct Android tester APK",
    "hero_title": "Pearl Wallet for Android is being tested.",
    "hero_summary": "PRL Wallet is a noncustodial Android wallet project for Pearl. This page is wired to release metadata so every build can update the version, date, download link, hash, changelog, and status without editing the homepage.",
    "primary_cta": "Download tester APK",
    "secondary_cta": "Verify the hash first",
    "above_fold_note": "Release data is populated from JSON now and XML as fallback. CI/manual builds emit both."
  },
  "source": {
    "repository": "https://github.com/Robin-s-AI-World/pearl-wallet-android",
    "commit": "${SOURCE_COMMIT}",
    "branch": "master",
    "ci_system": "manual",
    "ci_run_url": null
  },
  "distribution": {
    "channel": "direct-apk",
    "google_play_status": "not-active",
    "canonical_origin": "local-nginx-ui",
    "canonical_live_root": "/var/www/prldroid-wallet/current",
    "canonical_domain": "https://prldroid-wallet.robin.mba/",
    "shared_hosting_mirror": "downstream mirror for higher public traffic, not the canonical release authority"
  },
  "artifacts": [
    {
      "id": "android-apk-release",
      "platform": "android",
      "kind": "apk",
      "filename": "${APK_FILENAME}",
      "size_bytes": ${APK_SIZE},
      "sha256": "${APK_HASH}",
      "locations": [
        {
          "type": "web",
          "public": true,
          "url": "${APK_URL}"
        }
      ]
    }
  ],
  "verification": {
    "primary_artifact_id": "android-apk-release",
    "sha256_command": "sha256sum ${APK_FILENAME}",
    "expected_sha256": "${APK_HASH}"
  },
  "features": [
    {
      "title": "Manifest-driven landing page",
      "status": "available",
      "summary": "The homepage reads release metadata at runtime and fills version, dates, download URLs, hashes, status, features, and changelog."
    },
    {
      "title": "Direct signed APK distribution",
      "status": "available",
      "summary": "The tester APK is distributed from the site while app-store distribution is not active."
    },
    {
      "title": "Checksum verification",
      "status": "available",
      "summary": "The published SHA-256 is displayed beside the APK download so testers can confirm file integrity before installing."
    },
    {
      "title": "SPV wallet recovery",
      "status": "being-verified",
      "summary": "Import recovery, genesis birthday handling, and full balance discovery are under active repair and verification."
    },
    {
      "title": "Explorer preliminary balance",
      "status": "being-verified",
      "summary": "The app can display a provisional explorer balance for the visible receive address while local sync catches up. Full HD-wallet discovery remains a separate verification concern."
    },
    {
      "title": "Local canonical deployment",
      "status": "available",
      "summary": "The local nginx-ui deployment is the canonical site. Shared hosting can mirror it later for traffic, but the local release root remains authoritative."
    }
  ],
  "known_limitations": [
    "Working status: not-yet-first-confirmed-working-wallet",
    "Do not use tester APKs for meaningful funds unless a release is explicitly marked production-ready.",
    "Explorer preliminary balance is single-address and provisional until local wallet recovery is complete.",
    "Manual builds and CI builds must emit this manifest shape; index.html must not be hand-edited for release data."
  ],
  "changelog": {
    "entries": [
      {
        "version": "${VERSION}",
        "date": "${BUILT_AT}",
        "notes": [${CHANGELOG_NOTES}
        ]
      }
    ]
  }
}
EOF

# Clean up temp dir
rm -rf "$WORK_DIR"

echo "Manifest updated: ${APK_FILENAME} (${APK_SIZE} bytes, SHA-256 ${APK_HASH})"

# Deploy to Netlify
echo "Deploying to Netlify..."
netlify deploy --dir=. --site=02dc62c8-0007-4d66-9d33-99c9b4bd5be9 --prod

# Deploy to Vercel
echo "Deploying to Vercel..."
vercel deploy --prod --yes

echo "Done. v${VERSION} is live on Netlify and Vercel."
