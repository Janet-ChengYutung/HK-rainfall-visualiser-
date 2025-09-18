#!/usr/bin/env python3
"""
Example script demonstrating TSX background usage in pygame.
This shows how to create and use TSX files as backgrounds.
"""

import pygame
import xml.etree.ElementTree as ET
import os

def create_example_tsx(image_path, output_tsx_path, tile_width=1280, tile_height=720):
    """
    Create an example TSX file for a given image.
    
    Args:
        image_path: Path to the background image
        output_tsx_path: Where to save the TSX file
        tile_width: Width of the tile (default window width)
        tile_height: Height of the tile (default window height)
    """
    # Create TSX XML structure
    tileset = ET.Element('tileset')
    tileset.set('version', '1.5')
    tileset.set('tiledversion', '1.7.2')
    tileset.set('name', 'background')
    tileset.set('tilewidth', str(tile_width))
    tileset.set('tileheight', str(tile_height))
    tileset.set('tilecount', '1')
    tileset.set('columns', '1')
    
    # Add image element
    image_elem = ET.SubElement(tileset, 'image')
    image_elem.set('source', image_path)
    image_elem.set('width', str(tile_width))
    image_elem.set('height', str(tile_height))
    
    # Write to file
    tree = ET.ElementTree(tileset)
    ET.indent(tree, space=' ', level=0)
    tree.write(output_tsx_path, encoding='utf-8', xml_declaration=True)
    
    print(f"Created TSX file: {output_tsx_path}")
    print(f"References image: {image_path}")

def main():
    """Example usage of TSX background creation."""
    # Example: Create TSX for the existing TV image
    image_path = "image/TV - 1.png"
    tsx_path = "custom_background.tsx"
    
    if os.path.exists(image_path):
        create_example_tsx(image_path, tsx_path)
        print(f"\nYou can now use '{tsx_path}' as a background in Main.py")
        print("Update TSX_BACKGROUND_PATH in Main.py to point to this file.")
    else:
        print(f"Image not found: {image_path}")
        print("Please ensure the image exists before creating the TSX file.")

if __name__ == "__main__":
    main()