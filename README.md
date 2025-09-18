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
- Interactive and informative graphics (planned)
- **NEW:** TSX background support for custom backgrounds in the pygame window


## TSX Background Support 🎨

You can now use TSX (Tiled Tileset) files as backgrounds in the pygame window. TSX files are XML-based tileset files commonly used with the Tiled Map Editor.

### How to use TSX backgrounds:

1. Create or obtain a TSX file that references your background image
2. Place the TSX file in the project root directory
3. Update the `TSX_BACKGROUND_PATH` configuration in `Main.py`

### Example TSX file structure:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.5" tiledversion="1.7.2" name="background" tilewidth="1280" tileheight="720" tilecount="1" columns="1">
 <image source="image/your_background.png" width="1280" height="720"/>
</tileset>
```

The TSX background will automatically scale to fit the pygame window size.


## Status 🚧

Development is ongoing. Data download and basic animation features are in progress.


## How to Use 🛠️

1. Install required dependencies: `pip install pygame`
2. Run the main application: `python Main.py`
3. (Optional) Place a TSX file in the project directory for custom backgrounds

Instructions will be added once the first version is ready.


## License 📄

To be determined

