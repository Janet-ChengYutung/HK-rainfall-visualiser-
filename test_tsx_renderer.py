#!/usr/bin/env python3
"""
Test script for TSX background renderer.
"""

import pygame
import sys
import os
from tsx_background_renderer import create_tsx_background

def test_tsx_renderer():
    """Test the TSX background renderer functionality."""
    print("Testing TSX Background Renderer...")
    
    # Initialize pygame
    pygame.init()
    
    # Set a video mode for proper initialization
    screen = pygame.display.set_mode((800, 600), pygame.HIDDEN)
    
    # Test the renderer
    tsx_path = "animation.tsx"
    if not os.path.exists(tsx_path):
        print(f"TSX file not found: {tsx_path}")
        return False
    
    try:
        # Create background surface
        background = create_tsx_background(tsx_path, 800, 600)
        
        if background is None:
            print("Failed to create background surface")
            return False
        
        print("✓ Successfully created background surface")
        print(f"✓ Surface size: {background.get_size()}")
        print(f"✓ Surface format: {background.get_bitsize()}-bit")
        
        # Test saving the background as an image
        try:
            pygame.image.save(background, "test_tsx_background.png")
            print("✓ Successfully saved background as test_tsx_background.png")
        except Exception as e:
            print(f"✗ Failed to save background: {e}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing TSX renderer: {e}")
        return False
    
    finally:
        pygame.quit()

if __name__ == "__main__":
    success = test_tsx_renderer()
    print(f"\nTest {'PASSED' if success else 'FAILED'}")
    sys.exit(0 if success else 1)