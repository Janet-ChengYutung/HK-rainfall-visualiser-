# TSX Background Integration for Pygame

This document explains how to use TSX (TypeScript React) files as backgrounds in the pygame-based HK Rainfall Visualiser application.

## Overview

The TSX background renderer allows you to create beautiful, animated-style backgrounds using familiar TSX/React syntax and have them rendered as pygame backgrounds. While pygame cannot directly render TSX components, this solution parses TSX files and recreates equivalent visual elements using pygame's drawing functions.

## How It Works

1. **TSX Parsing**: The system reads your TSX file and extracts styling information including:
   - Linear and radial gradients
   - Floating particle effects
   - Text elements (headings and paragraphs)
   - Color schemes and positioning

2. **Pygame Rendering**: The extracted style information is converted to equivalent pygame drawing operations:
   - Gradients become interpolated color fills
   - Particles become semi-transparent circles
   - Text elements become rendered fonts with shadows

3. **Background Integration**: The rendered background is seamlessly integrated into the main application loop.

## Usage

### 1. Enable TSX Background

In `Main.py`, set the `TSX_BACKGROUND_PATH` variable:

```python
# Path to TSX background file (set to None to disable TSX background)
TSX_BACKGROUND_PATH = os.path.join(os.path.dirname(__file__), "animation.tsx")
```

To disable TSX backgrounds and use the default solid color background:

```python
TSX_BACKGROUND_PATH = None
```

### 2. Create Your TSX Background File

Create a TSX file (e.g., `animation.tsx`) with your desired background design:

```tsx
import React from 'react';

const Animation: React.FC = () => {
  return (
    <div 
      style={{
        width: '1280px',
        height: '720px',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        position: 'relative',
      }}
    >
      {/* Animated particles */}
      {[...Array(10)].map((_, i) => (
        <div
          key={i}
          style={{
            position: 'absolute',
            width: '20px',
            height: '20px',
            background: 'rgba(255,255,255,0.3)',
            borderRadius: '50%',
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
          }}
        />
      ))}
      
      {/* Title */}
      <h1>HK Rainfall Visualiser</h1>
      <p>Beautiful Weather Data</p>
    </div>
  );
};

export default Animation;
```

### 3. Supported TSX Features

The TSX background renderer currently supports:

#### Gradients
- **Linear gradients**: `background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'`
- **Radial gradients**: `background: 'radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 50%)'`

#### Particles
- **Floating elements**: Arrays of elements like `[...Array(10)].map(...)` are converted to particle systems
- **Circles**: Elements with `borderRadius: '50%'` become circular particles
- **Semi-transparency**: `rgba()` colors are properly handled

#### Text Elements
- **Headings**: `<h1>` tags become large, centered text with shadows
- **Paragraphs**: `<p>` tags become smaller subtitle text

#### Colors
- **Hex colors**: `#667eea`, `#764ba2`
- **RGB/RGBA**: `rgba(255,255,255,0.3)`

### 4. Running the Application

Simply run the main application as usual:

```bash
python Main.py
```

The console will show whether the TSX background was loaded successfully:

```
Loading TSX background from: animation.tsx
TSX background loaded successfully!
```

## Technical Details

### File Structure

```
HK-rainfall-visualiser-/
├── Main.py                    # Main application (modified)
├── tsx_background_renderer.py # TSX parsing and rendering engine
├── animation.tsx              # Your TSX background file
└── test_tsx_renderer.py       # Test utilities
```

### Key Components

- **`TSXBackgroundRenderer`**: Main class that handles TSX parsing and pygame rendering
- **`create_tsx_background()`**: Convenience function to create a background surface from a TSX file
- **Background caching**: Generated backgrounds are cached for performance

### Performance Considerations

- TSX backgrounds are rendered once at application startup
- The background surface is cached and reused each frame
- Window resizing will scale the background automatically
- No real-time TSX compilation - backgrounds are static once rendered

## Troubleshooting

### Common Issues

1. **"TSX file not found"**: Ensure your TSX file path is correct in `TSX_BACKGROUND_PATH`
2. **"Failed to load TSX background"**: Check that your TSX file contains valid styling syntax
3. **Blank background**: Verify your TSX contains supported style properties (gradients, colors, etc.)

### Debugging

Enable debug output by running the test:

```bash
python test_tsx_renderer.py
```

This will create a `test_tsx_background.png` file showing how your TSX background renders.

## Example TSX Backgrounds

### Simple Gradient
```tsx
<div style={{
  background: 'linear-gradient(45deg, #ff6b6b, #4ecdc4)',
  width: '1280px',
  height: '720px'
}}>
  <h1>Weather Dashboard</h1>
</div>
```

### Particle Effect
```tsx
<div style={{
  background: 'linear-gradient(135deg, #667eea, #764ba2)',
  width: '1280px',
  height: '720px'
}}>
  {[...Array(20)].map((_, i) => (
    <div key={i} style={{
      position: 'absolute',
      width: '15px',
      height: '15px',
      background: 'rgba(255,255,255,0.4)',
      borderRadius: '50%',
      left: `${(i * 47) % 100}%`,
      top: `${(i * 23) % 100}%`,
    }} />
  ))}
</div>
```

## Limitations

- Animation properties (keyframes, transitions) are not rendered - backgrounds are static
- Complex CSS properties may not be supported
- React component logic (hooks, state) is ignored - only visual styling is processed
- Limited to basic gradients, text, and particle effects

This solution provides a bridge between modern web development (TSX/React) and pygame graphics, allowing developers to design backgrounds using familiar tools while maintaining pygame compatibility.