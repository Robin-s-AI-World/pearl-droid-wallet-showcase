#!/usr/bin/env bash
set -euo pipefail

# Publish a signed APK from the canonical dist/ to GitHub Releases.
# APK only — no AAB, no debug symbols, no source (per release policy).
#
# Usage: ./scripts/publish-release-to-github.sh <version> [path-to-dist]
# Example: ./scripts/publish-release-to-github.sh 1.124.08366 /home/robin/Desktop/github/rebots-online/pearl-wallet-android/dist

VERSION="${1:?Usage: $0 <version> [path-to-dist]}"
DIST_DIR="${2:-/home/robin/Desktop/github/rebots-online/pearl-wallet-android/dist}"
REPO="rebots-online/pearl-wallet-releases"
APK_FILENAME="pearl-wallet-android-v${VERSION}-release-signed.apk"
APK_PATH="${DIST_DIR}/${APK_FILENAME}"
NOTES_FILE="${DIST_DIR}/RELEASE_NOTES-v${VERSION}.md"

if [[ ! -f "$APK_PATH" ]]; then
  echo "ERROR: APK not found at ${APK_PATH}"
  exit 1
fi

# Use RELEASE_NOTES if it has real content, otherwise prompt for notes
NOTES_ARG=""
if [[ -f "$NOTES_FILE" ]] && [[ -s "$NOTES_FILE" ]]; then
  NOTES_ARG="--notes-file ${NOTES_FILE}"
else
  echo "No release notes file found at ${NOTES_FILE}."
  echo "Enter release notes (Ctrl-D to finish):"
  NOTES_ARG="--notes-file -"
fi

echo "Publishing ${APK_FILENAME} to GitHub Releases..."
echo "  Repo: ${REPO}"
echo "  Tag:  v${VERSION}"
echo "  APK:  ${APK_PATH} ($(stat -c %s "$APK_PATH") bytes)"
echo ""

gh release create "v${VERSION}" \
  --repo "$REPO" \
  --title "PRL Wallet v${VERSION}" \
  $NOTES_ARG \
  "$APK_PATH"

echo ""
echo "Done. Release published: https://github.com/${REPO}/releases/tag/v${VERSION}"
echo ""
echo "Next step: run update-pearl-showcase-release.sh ${VERSION} to update the showcase site."
