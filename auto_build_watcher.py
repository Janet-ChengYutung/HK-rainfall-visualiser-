#!/usr/bin/env python3
"""Simple file watcher that runs the PyInstaller build script whenever
`Main.py` or other tracked files change. Useful for development so the
packaged app is kept in sync with source edits.

Usage: python auto_build_watcher.py

Requirements: watchdog (pip install watchdog)
"""
import subprocess
import sys
import time
from pathlib import Path

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except Exception:
    print("Please install watchdog: pip install watchdog")
    sys.exit(1)

ROOT = Path(__file__).parent
WATCH_PATTERNS = ["Main.py", "animationtest.py", "viewchart.py"]
BUILD_SCRIPT = ROOT / "build_pyinstaller.sh"

class ChangeHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self._last = 0

    def on_any_event(self, event):
        # debounce
        now = time.time()
        if now - self._last < 1.0:
            return
        self._last = now
        p = Path(event.src_path)
        if p.name in WATCH_PATTERNS:
            print(f"Detected change in {p.name}, running build...")
            try:
                subprocess.check_call([str(BUILD_SCRIPT)])
                print("Build finished")
            except subprocess.CalledProcessError as e:
                print("Build failed:", e)

if __name__ == '__main__':
    obs = Observer()
    handler = ChangeHandler()
    obs.schedule(handler, str(ROOT), recursive=False)
    obs.start()
    print("Watching for changes. Ctrl-C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        obs.stop()
    obs.join()
