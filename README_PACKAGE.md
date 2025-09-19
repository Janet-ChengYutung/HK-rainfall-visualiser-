Packaging & running
====================

This project is a small Pygame app. The following files are helper artifacts to make it easy for others to run without VS Code.

Quick run (recommended)
-----------------------
1. Create a Python 3.11+ virtualenv (recommended) and install dependencies:

   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

2. Run the application:

   ./run.sh


Build a standalone app (optional)
--------------------------------
We recommend using PyInstaller to create a single-binary app. Install PyInstaller in your venv:

   pip install pyinstaller

Then run the provided build script which includes images, fonts and data files:

   ./build_pyinstaller.sh

On success you'll find a single file under `dist/` named `Main` (or `Main.exe` on Windows). To run it:

   ./dist/Main

Notes:
- The produced file is a self-contained executable; on macOS you may need to give it execute permission: `chmod +x dist/Main`.
- PyInstaller bundles many libraries; the resulting file can be large.
- For distribution on macOS you may need to code-sign and notarize the binary.

CI Builds (macOS & Windows)
---------------------------
This repository includes a GitHub Actions workflow that builds macOS and Windows executables using PyInstaller.

To use it:
1. Push your branch or open a PR against `main`.
2. After the workflow completes, go to the workflow run and download the `macos-build` or `windows-build` artifact which contains the `dist/` folder with the produced binary.

Note: The Windows build will produce an `.exe` file; macOS build will produce a `Main` binary. You may still need to sign/notarize for distribution on macOS.

Packaging into platform installers
---------------------------------
macOS (.app + optional DMG)

1. Build a one-dir bundle with PyInstaller (the build script does onefile by default; for .app use one-dir):

   pyinstaller Main.py --onedir --noconfirm --windowed

2. Run the helper to create a minimal `.app` bundle:

   ./package_macos_app.sh --name "HK Rainfall"

3. Optionally create a DMG (requires `hdiutil`):

   hdiutil create -volname 'HK Rainfall' -srcfolder 'dist/HKRain.app' -ov -format UDZO dist/HKRain.dmg

Windows (NSIS installer)

1. Build the EXE (onefile) using PyInstaller (CI already does this):

   pyinstaller Main.py --onefile --noconfirm --windowed

2. Run makensis (NSIS) to create an installer. If makensis is available locally:

   makensis nsis_installer.nsi

Or use the provided helper (on environments with makensis):

   ./windows_packager.sh

The NSIS script is a minimal template — adjust to add custom icons, registry entries, or additional files.

Auto-rebuild on source changes (dev)
-----------------------------------
If you frequently edit `Main.py` and want the packaged app updated automatically, use the watcher script:

1. Install the watcher dependency:

   pip install watchdog

2. Run the watcher (it calls `build_pyinstaller.sh` when files change):

   python auto_build_watcher.py

This will re-run the build script when `Main.py`, `animationtest.py`, or `viewchart.py` change.

Troubleshooting
---------------
- If fonts or images fail to load, check paths under the project `image/` and `GoogleSansCode-VariableFont_wght.ttf` file.
- If Pygame emits SDL errors on macOS, ensure XQuartz or other system libraries are installed and Python is not sandboxed.
