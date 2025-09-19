#!/usr/bin/env bash
set -euo pipefail

# Create a macOS .app bundle from a PyInstaller one-dir build.
# Usage: ./package_macos_app.sh [--name "HK Rainfall"]
# Requires: pyinstaller, optionally hdiutil (macOS) to create a DMG.

APP_NAME="HK Rainfall"
BUNDLE_NAME="HKRain.app"
OUT_DIR=dist
PYINSTALLER=${PYINSTALLER:-pyinstaller}
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --name) APP_NAME="$2"; shift 2;;
    --bundle) BUNDLE_NAME="$2"; shift 2;;
    *) echo "Unknown arg: $1"; exit 1;;
  esac
done

echo "Building one-dir with PyInstaller..."
${PYINSTALLER} Main.py --onedir --noconfirm --windowed

if [ ! -d "$OUT_DIR" ]; then
  echo "PyInstaller didn't produce $OUT_DIR. Exiting." >&2
  exit 2
fi

APP_BUNDLE="${OUT_DIR}/${BUNDLE_NAME}"
echo "Creating app bundle at: $APP_BUNDLE"

# Prepare bundle structure
rm -rf "$APP_BUNDLE"
mkdir -p "$APP_BUNDLE/Contents/MacOS"
mkdir -p "$APP_BUNDLE/Contents/Resources"

# Minimal Info.plist
cat > "$APP_BUNDLE/Contents/Info.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleName</key>
  <string>${APP_NAME}</string>
  <key>CFBundleIdentifier</key>
  <string>org.example.hkrain</string>
  <key>CFBundleVersion</key>
  <string>1.0</string>
  <key>CFBundleExecutable</key>
  <string>Main</string>
  <key>LSMinimumSystemVersion</key>
  <string>10.12</string>
</dict>
</plist>
PLIST

# Copy the one-dir build contents into Resources and use the main binary as the executable
ONE_DIR="${OUT_DIR}/Main"
if [ ! -d "$ONE_DIR" ]; then
  echo "Expected PyInstaller one-dir at $ONE_DIR" >&2
  exit 3
fi

# Copy entire one-dir tree into Resources
cp -R "$ONE_DIR/"* "$APP_BUNDLE/Contents/Resources/"

# Expect the executable in the one-dir under 'Main' (PyInstaller default on macOS)
if [ -f "$ONE_DIR/Main" ]; then
  cp "$ONE_DIR/Main" "$APP_BUNDLE/Contents/MacOS/Main"
elif [ -f "$ONE_DIR/Main.exe" ]; then
  # fallback
  cp "$ONE_DIR/Main.exe" "$APP_BUNDLE/Contents/MacOS/Main"
fi

chmod +x "$APP_BUNDLE/Contents/MacOS/Main"

echo "App bundle created: $APP_BUNDLE"

echo "You can optionally create a DMG with: hdiutil create -volname '${APP_NAME}' -srcfolder '$APP_BUNDLE' -ov -format UDZO ${OUT_DIR}/${BUNDLE_NAME}.dmg"
