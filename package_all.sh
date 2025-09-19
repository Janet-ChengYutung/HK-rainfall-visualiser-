#!/usr/bin/env bash
set -euo pipefail

# package_all.sh - central wrapper to build and package the app for distribution
# Usage: ./package_all.sh [--force-onedir] [--make-app] [--make-installer]
#   --force-onedir : use --onedir (faster during dev)
#   --make-app     : create mac .app bundle (calls package_macos_app.sh)
#   --make-installer: run Windows NSIS packaging (invokes makensis via windows_packager.sh)

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV="${ROOT_DIR}/../Data-visualization/.venv"
PYINSTALLER=""
FORCE_ONEDIR=0
MAKE_APP=0
MAKE_INSTALLER=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force-onedir) FORCE_ONEDIR=1; shift;;
    --make-app) MAKE_APP=1; shift;;
    --make-installer) MAKE_INSTALLER=1; shift;;
    *) echo "Unknown arg: $1"; exit 1;;
  esac
done

# find pyinstaller
if [ -x "$VENV/bin/pyinstaller" ]; then
  PYINSTALLER="$VENV/bin/pyinstaller"
elif [ -x "${ROOT_DIR}/.venv/bin/pyinstaller" ]; then
  PYINSTALLER="${ROOT_DIR}/.venv/bin/pyinstaller"
else
  PYINSTALLER="$(which pyinstaller 2>/dev/null || true)"
fi
if [ -z "$PYINSTALLER" ]; then
  echo "pyinstaller not found. Install it in your venv or on PATH."
  exit 2
fi

# choose mode
if [ "$FORCE_ONEDIR" -eq 1 ]; then
  MODE="--onedir"
else
  MODE="--onefile"
fi

echo "Using pyinstaller: $PYINSTALLER"

echo "Running build_pyinstaller.sh (this will read package_files.txt)"
# call the existing build script which will build and zip artifact
"${ROOT_DIR}/build_pyinstaller.sh"

# optionally build .app
if [ "$MAKE_APP" -eq 1 ]; then
  if [ -x "${ROOT_DIR}/package_macos_app.sh" ]; then
    echo "Creating .app bundle"
    "${ROOT_DIR}/package_macos_app.sh"
  else
    echo "package_macos_app.sh not found or not executable"
  fi
fi

# optionally create Windows installer (requires makensis on system)
if [ "$MAKE_INSTALLER" -eq 1 ]; then
  if [ -x "${ROOT_DIR}/windows_packager.sh" ]; then
    echo "Creating Windows installer via NSIS"
    "${ROOT_DIR}/windows_packager.sh"
  else
    echo "windows_packager.sh not found or not executable"
  fi
fi

echo "All done. Packaged artifacts (if any) are in packages/ and dist/"
