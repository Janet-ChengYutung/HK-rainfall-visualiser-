"""
TSX Background Renderer for Pygame

This module provides functionality to interpret TSX files and render equivalent
backgrounds in pygame. Since pygame cannot directly render TSX, this utility
extracts styling information and recreates the visual elements using pygame.
"""

import pygame
import re
import math
import json
from typing import Dict, List, Tuple, Optional
import colorsys

class TSXBackgroundRenderer:
    def __init__(self, width: int = 1280, height: int = 720):
        self.width = width
        self.height = height
        self.surface = None
        
    def parse_tsx_file(self, tsx_path: str) -> Dict:
        """Parse a TSX file and extract visual styling information."""
        try:
            with open(tsx_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"TSX file not found: {tsx_path}")
            return {}
            
        # Extract style information using regex patterns
        styles = self._extract_styles(content)
        return styles
    
    def _extract_styles(self, content: str) -> Dict:
        """Extract styling information from TSX content."""
        styles = {
            'background': None,
            'gradients': [],
            'particles': [],
            'text_elements': [],
            'animations': []
        }
        
        # Extract background gradients
        gradient_pattern = r'background:\s*[\'"]linear-gradient\([^)]+\)[\'"]'
        gradients = re.findall(gradient_pattern, content)
        for gradient in gradients:
            parsed_gradient = self._parse_gradient(gradient)
            if parsed_gradient:
                styles['gradients'].append(parsed_gradient)
        
        # Extract radial gradients
        radial_pattern = r'background:\s*[\'"]radial-gradient\([^)]+\)[\'"]'
        radial_gradients = re.findall(radial_pattern, content)
        for gradient in radial_gradients:
            parsed_gradient = self._parse_radial_gradient(gradient)
            if parsed_gradient:
                styles['gradients'].append(parsed_gradient)
        
        # Extract particle information (floating elements)
        particle_pattern = r'\[\.\.\.Array\((\d+)\)\]'
        particle_matches = re.findall(particle_pattern, content)
        if particle_matches:
            styles['particles'] = [{'count': int(count)} for count in particle_matches]
        
        # Extract text elements
        text_pattern = r'<h1[^>]*>([^<]+)</h1>'
        text_matches = re.findall(text_pattern, content)
        styles['text_elements'].extend([{'text': text, 'type': 'h1'} for text in text_matches])
        
        text_pattern = r'<p[^>]*>([^<]+)</p>'
        text_matches = re.findall(text_pattern, content)
        styles['text_elements'].extend([{'text': text, 'type': 'p'} for text in text_matches])
        
        return styles
    
    def _parse_gradient(self, gradient_str: str) -> Optional[Dict]:
        """Parse a linear gradient string."""
        # Extract direction and colors
        match = re.search(r'linear-gradient\(([^)]+)\)', gradient_str)
        if not match:
            return None
            
        parts = match.group(1).split(',')
        direction = parts[0].strip()
        colors = []
        
        for part in parts[1:]:
            color_match = re.search(r'#([0-9a-fA-F]{6})', part)
            if color_match:
                hex_color = color_match.group(1)
                colors.append(self._hex_to_rgb(hex_color))
        
        return {
            'type': 'linear',
            'direction': direction,
            'colors': colors
        }
    
    def _parse_radial_gradient(self, gradient_str: str) -> Optional[Dict]:
        """Parse a radial gradient string."""
        match = re.search(r'radial-gradient\(([^)]+)\)', gradient_str)
        if not match:
            return None
            
        parts = match.group(1).split(',')
        colors = []
        
        for part in parts:
            color_match = re.search(r'rgba?\(([^)]+)\)', part)
            if color_match:
                rgba_values = [float(x.strip()) for x in color_match.group(1).split(',')]
                if len(rgba_values) >= 3:
                    colors.append(tuple(int(x) if i < 3 else x for i, x in enumerate(rgba_values[:4])))
        
        return {
            'type': 'radial',
            'colors': colors
        }
    
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple."""
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def render_background(self, tsx_path: str) -> pygame.Surface:
        """Render a pygame surface based on TSX file."""
        styles = self.parse_tsx_file(tsx_path)
        
        # Create surface
        self.surface = pygame.Surface((self.width, self.height))
        self.surface = self.surface.convert()
        
        # Render gradients
        self._render_gradients(styles.get('gradients', []))
        
        # Render particles
        self._render_particles(styles.get('particles', []))
        
        # Render text elements
        self._render_text_elements(styles.get('text_elements', []))
        
        return self.surface
    
    def _render_gradients(self, gradients: List[Dict]):
        """Render gradient backgrounds."""
        for gradient in gradients:
            if gradient['type'] == 'linear':
                self._render_linear_gradient(gradient)
            elif gradient['type'] == 'radial':
                self._render_radial_gradient(gradient)
    
    def _render_linear_gradient(self, gradient: Dict):
        """Render a linear gradient."""
        colors = gradient.get('colors', [(100, 100, 200), (120, 75, 162)])
        direction = gradient.get('direction', '135deg')
        
        if len(colors) < 2:
            colors = [(100, 100, 200), (120, 75, 162)]  # Default gradient
        
        # Simple linear gradient implementation
        for y in range(self.height):
            t = y / self.height
            # Interpolate between first and last color
            color = self._interpolate_color(colors[0], colors[-1], t)
            pygame.draw.line(self.surface, color, (0, y), (self.width, y))
    
    def _render_radial_gradient(self, gradient: Dict):
        """Render a radial gradient overlay."""
        colors = gradient.get('colors', [(255, 255, 255, 25)])
        
        if not colors:
            return
        
        # Create a semi-transparent surface for the radial effect
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Draw radial gradient effect using circles
        center_x, center_y = self.width * 0.3, self.height * 0.3
        max_radius = min(self.width, self.height) // 2
        
        for radius in range(max_radius, 0, -5):
            alpha = int(25 * (1 - radius / max_radius))
            color = colors[0][:3] + (alpha,) if len(colors[0]) > 3 else colors[0] + (alpha,)
            # Use regular pygame.draw.circle instead of gfxdraw
            pygame.draw.circle(overlay, color[:3], (int(center_x), int(center_y)), radius)
        
        self.surface.blit(overlay, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
    
    def _render_particles(self, particles: List[Dict]):
        """Render floating particles."""
        for particle_group in particles:
            count = particle_group.get('count', 10)
            for i in range(count):
                # Generate pseudo-random positions based on index for consistency
                x = int((i * 17 + 42) % self.width)
                y = int((i * 23 + 67) % self.height)
                size = int(10 + (i * 7) % 20)
                
                # Semi-transparent white circles - use regular draw.circle
                color = (255, 255, 255)  # Use RGB, handle alpha separately
                
                # Create a surface for the particle with alpha
                particle_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                pygame.draw.circle(particle_surf, color, (size, size), size)
                particle_surf.set_alpha(76)  # Set alpha for transparency
                
                self.surface.blit(particle_surf, (x - size, y - size))
    
    def _render_text_elements(self, text_elements: List[Dict]):
        """Render text elements."""
        pygame.font.init()
        
        for element in text_elements:
            text = element.get('text', '')
            text_type = element.get('type', 'p')
            
            if text_type == 'h1':
                font_size = 48
                font = pygame.font.Font(None, font_size)
            else:
                font_size = 24
                font = pygame.font.Font(None, font_size)
            
            # Render text with shadow effect
            shadow_color = (0, 0, 0, 128)
            text_color = (255, 255, 255)
            
            # Render shadow
            shadow_surf = font.render(text, True, (0, 0, 0))
            text_surf = font.render(text, True, text_color)
            
            # Center the text
            text_rect = text_surf.get_rect()
            x = (self.width - text_rect.width) // 2
            y = (self.height - text_rect.height) // 2
            
            if text_type == 'h1':
                y -= 30  # Move title up a bit
            else:
                y += 30  # Move subtitle down a bit
            
            # Draw shadow slightly offset
            self.surface.blit(shadow_surf, (x + 2, y + 2))
            self.surface.blit(text_surf, (x, y))
    
    def _interpolate_color(self, color1: Tuple[int, int, int], color2: Tuple[int, int, int], t: float) -> Tuple[int, int, int]:
        """Interpolate between two colors."""
        r = int(color1[0] + (color2[0] - color1[0]) * t)
        g = int(color1[1] + (color2[1] - color1[1]) * t)
        b = int(color1[2] + (color2[2] - color1[2]) * t)
        return (r, g, b)

def create_tsx_background(tsx_path: str, width: int = 1280, height: int = 720) -> Optional[pygame.Surface]:
    """
    Convenience function to create a pygame background from a TSX file.
    
    Args:
        tsx_path: Path to the TSX file
        width: Width of the background surface
        height: Height of the background surface
    
    Returns:
        pygame.Surface with the rendered background, or None if failed
    """
    try:
        renderer = TSXBackgroundRenderer(width, height)
        return renderer.render_background(tsx_path)
    except Exception as e:
        print(f"Error creating TSX background: {e}")
        return None