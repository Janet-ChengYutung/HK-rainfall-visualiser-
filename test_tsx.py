#!/usr/bin/env python3
"""
Test script to verify TSX background loading functionality.
"""

import pygame
import sys
import os

# Import the TSX class from Main.py
sys.path.insert(0, os.path.dirname(__file__))
from Main import TSXBackground

def test_tsx_loading():
    """Test TSX background loading with a minimal display."""
    print("Testing TSX background loading...")
    
    # Initialize pygame with a minimal display for image loading
    pygame.init()
    screen = pygame.display.set_mode((1, 1))  # Minimal display mode
    
    # Test with the sample TSX file
    tsx_files_to_test = [
        "sample_background.tsx",
        "custom_background.tsx"
    ]
    
    success_count = 0
    
    for tsx_file in tsx_files_to_test:
        if os.path.exists(tsx_file):
            print(f"\nTesting {tsx_file}...")
            tsx_bg = TSXBackground(tsx_file)
            
            if tsx_bg.is_loaded():
                print(f"✓ Successfully loaded TSX background from {tsx_file}")
                print(f"  - Tile size: {tsx_bg.tile_width}x{tsx_bg.tile_height}")
                print(f"  - Image size: {tsx_bg.image_width}x{tsx_bg.image_height}")
                success_count += 1
            else:
                print(f"✗ Failed to load TSX background from {tsx_file}")
        else:
            print(f"⚠ TSX file not found: {tsx_file}")
    
    pygame.quit()
    
    print(f"\nTSX loading test completed. {success_count}/{len(tsx_files_to_test)} files loaded successfully.")
    return success_count > 0

if __name__ == "__main__":
    success = test_tsx_loading()
    sys.exit(0 if success else 1)