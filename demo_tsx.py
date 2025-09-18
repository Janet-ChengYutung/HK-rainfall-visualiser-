#!/usr/bin/env python3
"""
Demonstration of TSX background functionality.
This creates a minimal pygame window showing TSX background loading.
"""

import pygame
import sys
import os
from Main import TSXBackground

def demo_tsx_background():
    """Demonstrate TSX background in a simple pygame window."""
    
    # Initialize pygame
    pygame.init()
    
    # Create a small demo window
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSX Background Demo")
    clock = pygame.time.Clock()
    
    # Load TSX background
    tsx_files = ["sample_background.tsx", "custom_background.tsx"]
    tsx_background = None
    
    for tsx_file in tsx_files:
        if os.path.exists(tsx_file):
            tsx_background = TSXBackground(tsx_file)
            if tsx_background.is_loaded():
                print(f"Loaded TSX background: {tsx_file}")
                break
    
    # Main demo loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Draw background
        if tsx_background and tsx_background.is_loaded():
            tsx_background.draw(screen, scale=(WIDTH, HEIGHT))
        else:
            screen.fill((100, 150, 200))  # Default blue background
        
        # Draw info text  
        font = pygame.font.Font(None, 36)
        if tsx_background and tsx_background.is_loaded():
            text = font.render("TSX Background Loaded!", True, (255, 255, 255))
        else:
            text = font.render("No TSX Background Found", True, (255, 255, 255))
        
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text, text_rect)
        
        # Instructions
        font_small = pygame.font.Font(None, 24)
        instruction = font_small.render("Press ESC to exit", True, (255, 255, 255))
        screen.blit(instruction, (10, HEIGHT - 30))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    print("Demo completed.")

if __name__ == "__main__":
    demo_tsx_background()