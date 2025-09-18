#!/usr/bin/env python3
"""
Demo script to create a visual comparison showing TSX background vs default background.
"""

import pygame
import sys
import os
from tsx_background_renderer import create_tsx_background

def create_demo_comparison():
    """Create a side-by-side comparison of TSX background vs default background."""
    print("Creating TSX background demo comparison...")
    
    # Create demo surface
    demo_width, demo_height = 1280, 720
    
    # Initialize pygame
    pygame.init()
    
    # Set a video mode for proper initialization
    screen = pygame.display.set_mode((demo_width * 2, demo_height), pygame.HIDDEN)
    demo_surface = pygame.Surface((demo_width * 2, demo_height))  # Side by side
    
    # Create default background (left side)
    BG_COLOR = (180, 180, 180)
    default_bg = pygame.Surface((demo_width, demo_height))
    default_bg.fill(BG_COLOR)
    
    # Add label for default background
    pygame.font.init()
    font = pygame.font.Font(None, 48)
    label = font.render("Default Background", True, (60, 60, 60))
    label_rect = label.get_rect(center=(demo_width // 2, 100))
    default_bg.blit(label, label_rect)
    
    # Create TSX background (right side)
    tsx_bg = create_tsx_background("animation.tsx", demo_width, demo_height)
    if tsx_bg is None:
        # Fallback if TSX loading fails
        tsx_bg = pygame.Surface((demo_width, demo_height))
        tsx_bg.fill((100, 100, 200))
        error_label = font.render("TSX Background (Failed to Load)", True, (255, 255, 255))
        error_rect = error_label.get_rect(center=(demo_width // 2, demo_height // 2))
        tsx_bg.blit(error_label, error_rect)
    else:
        # Add label for TSX background
        label = font.render("TSX Background", True, (255, 255, 255))
        label_rect = label.get_rect(center=(demo_width // 2, 50))
        # Create a semi-transparent background for the label
        label_bg = pygame.Surface((label.get_width() + 20, label.get_height() + 10), pygame.SRCALPHA)
        label_bg.fill((0, 0, 0, 128))
        tsx_bg.blit(label_bg, (label_rect.x - 10, label_rect.y - 5))
        tsx_bg.blit(label, label_rect)
    
    # Combine both backgrounds
    demo_surface.blit(default_bg, (0, 0))
    demo_surface.blit(tsx_bg, (demo_width, 0))
    
    # Add separator line
    pygame.draw.line(demo_surface, (255, 255, 255), (demo_width, 0), (demo_width, demo_height), 4)
    
    # Save the comparison
    try:
        pygame.image.save(demo_surface, "tsx_background_comparison.png")
        print("✓ Created tsx_background_comparison.png")
        print(f"✓ Comparison image size: {demo_surface.get_size()}")
        return True
    except Exception as e:
        print(f"✗ Failed to save comparison image: {e}")
        return False
    
    finally:
        pygame.quit()

if __name__ == "__main__":
    os.environ['SDL_VIDEODRIVER'] = 'dummy'  # Headless mode
    success = create_demo_comparison()
    print(f"\nDemo {'COMPLETED' if success else 'FAILED'}")
    sys.exit(0 if success else 1)