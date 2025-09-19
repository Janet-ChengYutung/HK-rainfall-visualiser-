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

