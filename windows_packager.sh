#!/usr/bin/env bash
set -euo pipefail

if ! command -v makensis >/dev/null 2>&1; then
  echo "makensis not found. Install NSIS or run this on a Windows runner that has NSIS installed."
  exit 1
fi

makensis nsis_installer.nsi
echo "Installer created: HkRainfallInstaller.exe"
