# Combined text files from the repository

---

File: package_files.txt

# List of files or folders to include in the PyInstaller bundle
# Format: source_path:target_relative_path
# Lines starting with # are ignored

image:image
rainfall_charts:rainfall_charts
monthlyElement.xml:.
GoogleSansCode-VariableFont_wght.ttf:.

---

File: requirements.txt

pip-requirements

pygame==2.6.1
watchdog==3.0.0

---

File: Data_visualization/testing_readme.txt

## testing.py

This script is used to test tide data scraping and processing functions. It loads environment variables, fetches tide data from a specified URL, and performs basic analysis such as calculating maximum, minimum, and average tide values.

### Usage

Before running, set the `URL` environment variable (either in a `.env` file or in your shell):

.env file example:

URL=https://your-tide-data-url

Or in terminal:

export URL=https://your-tide-data-url
python Data_visualization/testing.py

### Features

- Loads environment variables using `python-dotenv`
- Fetches tide data from a remote source
- Calculates and prints tide statistics

### Dependencies

- requests
- python-dotenv

Install dependencies with:

pip install requests python-dotenv

---

File: Data_visualization/#readme.txt

## draw_svg.py

This script demonstrates how to create SVG graphics and simple data visualizations using the `drawsvg` Python library. It generates several SVG files:
- `irregular-polygon.svg`: An example of an irregular polygon.
- `geometric-shapes.svg`: Contains geometric shapes like rectangles, circles, and lines.
- `tide-chart.svg`: A simple bar chart visualizing tide statistics (sample data or loaded from variables).

### Usage

Run the script:

python Data_visualization/draw_svg.py

The generated SVG files can be opened in any web browser or SVG viewer.

### Dependencies

The following Python packages are required:
- drawsvg
- lxml
- matplotlib
- requests
- python-dotenv

Install all dependencies with:

pip install drawsvg lxml matplotlib requests python-dotenv

---

# Notes
- Originals of these files remain in place. If you want me to delete or archive them after verification, tell me and I'll remove them or move them into an `archive/` folder.
- I kept the file headers so it's easy to see where each original text came from.
