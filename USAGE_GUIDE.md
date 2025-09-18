# TSX Background Usage Guide

## Quick Start

1. **Create a TSX file** pointing to your background image:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.5" name="background" tilewidth="1280" tileheight="720" tilecount="1" columns="1">
 <image source="image/your_background.png" width="1280" height="720"/>
</tileset>
```

2. **Update Main.py configuration**:
```python
TSX_BACKGROUND_PATH = "your_background.tsx"
```

3. **Run the application**:
```bash
python Main.py
```

## Helper Scripts

### Generate TSX from Image
```bash
python tsx_example.py
```

### Test TSX Loading
```bash
python test_tsx.py
```

### Demo TSX Functionality
```bash
python demo_tsx.py
```

## TSX File Structure

```
your_project/
├── Main.py                 # Main application
├── your_background.tsx     # Your TSX file
├── image/
│   └── background.png      # Your background image
└── ...
```

## Features

- ✅ Automatic scaling to window size
- ✅ Fallback to default background if TSX not found
- ✅ Support for relative image paths
- ✅ Standard Tiled Map Editor TSX format
- ✅ Error handling and validation

## Example TSX Files Included

- `sample_background.tsx` - Uses existing TV image
- `custom_background.tsx` - Generated example file

Both files demonstrate the correct TSX format and can be used as templates for your own backgrounds.