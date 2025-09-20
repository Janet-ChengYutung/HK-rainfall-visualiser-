# HK Rainfall Visualiser

The HK Rainfall Visualiser is a small desktop application that animates historical Hong Kong monthly rainfall data and lets you open an external rainfall chart viewer.

Status
------
- The main application (`Main.py`) is finished and ready to run.

Run locally
-----------
1. Create and activate a Python 3.11+ virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python Main.py
```

Packaging and Downloads
-----------------------
- CI builds for macOS and Windows create packaged executables and publish them as a GitHub Release titled "HK Rainfall Visualiser". Check the repository's Releases page to download the artifacts.
- Each Release contains per-platform files:
  - `HK_Rainfall_Visualiser_<platform>_executable` — the executable you run
  - `HK_Rainfall_Visualiser_<platform>_assets.zip` — runtime assets required next to the executable (image/, data/monthlyElement.xml, font)

Packaging helpers (archived)
---------------------------
- Packaging scripts and helper files were moved to `packagenotwork/` to keep the repository root focused on runtime code. If you need to rebuild the packages, see that directory.

Notes
-----
- The repository excludes Python bytecode caches (`__pycache__`, `*.pyc`). These are not tracked in git.
- If you want the release process changed (e.g., only publish on tags), or a small README added inside the assets zip, tell me and I will update the workflow.

Contact & credits
-----------------
See file headers for author credits.
# HK Rainfall Visualiser 🚧 (WIP)


🌧️ HK Rainfall Visualiser

This project is a work-in-progress Python tool for visualizing the Monthly Total Rainfall (mm) at the Hong Kong Observatory.


## Project Overview 📊

- **Goal:** Create an animated visualizer to explore historical rainfall data for Hong Kong.
- **Data Source:** Monthly rainfall data will be downloaded from the official Hong Kong Observatory website: [Hong Kong Observatory Monthly Rainfall Data 🌐](https://www.hko.gov.hk/en/cis/monthlyElement.htm?stn=HKO&ele=RF)
- **Technology:** Python 🐍 (data processing and animation)


## Features ✨

- Download and parse rainfall data from the web
- Generate animated visualizations of monthly rainfall trends
- **NEW: TSX Background Support** - Use TypeScript React components as pygame backgrounds
- Interactive and informative graphics (planned)


## Status 🚧

Development is ongoing. Data download and basic animation features are in progress.


## How to Use 🛠️

### Basic Usage
```bash
python Main.py
```

### TSX Background Feature
You can now use TSX (TypeScript React) files as animated backgrounds! 

1. **Enable TSX backgrounds** by setting `TSX_BACKGROUND_PATH` in `Main.py`
2. **Create your TSX file** with gradients, particles, and text elements
3. **Run the application** - the TSX will be converted to a pygame background

For detailed instructions, see [README_TSX_BACKGROUND.md](README_TSX_BACKGROUND.md)

### Packaging and running outside VS Code
If you want to distribute or run the app without VS Code, see `README_PACKAGE.md` for a short guide and helper scripts (`run.sh`, `build_pyinstaller.sh`).

**Example TSX background:**
```tsx
<div style={{
  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  width: '1280px', height: '720px'
}}>
  {[...Array(10)].map((_, i) => (
    <div key={i} style={{
      position: 'absolute',
      background: 'rgba(255,255,255,0.3)',
      borderRadius: '50%',
      // ... particle styling
    }} />
  ))}
  <h1>HK Rainfall Visualiser</h1>
</div>
```


## License 📄

To be determined

