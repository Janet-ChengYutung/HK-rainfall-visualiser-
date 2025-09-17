
import pygame
import pygame.gfxdraw
import sys
import math
import os
import time

# ---------- Image Button Class ----------
class ImageButton:
    def __init__(self, rect, image_on_path, image_off_path):
        self.rect = pygame.Rect(rect)
        self.image_on = pygame.image.load(image_on_path).convert_alpha()
        self.image_off = pygame.image.load(image_off_path).convert_alpha()
        self.down = False
        self.callback = None

    def draw(self, surface):
        img = self.image_off if self.down else self.image_on
        img_scaled = pygame.transform.smoothscale(img, (self.rect.width, self.rect.height))
        surface.blit(img_scaled, (self.rect.x, self.rect.y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.down = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.down and self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback(self)
            self.down = False
"""
ui_with_temporary_color_and_font.py

- Uses external PNG icons for buttons (start/stop/reload) stored in ICON_BASE_PATH.
- When a button is clicked, its icon variant changes for 1.0 second (start -> green; stop -> red; reload stays black).
- Loads a custom font file if FONT_PATH points to a TTF/OTF; otherwise falls back to a system font.
- If PNG icon is missing, falls back to vector drawing.
"""

# ---------- Configuration ----------
WIDTH, HEIGHT = 1280, 720
FPS = 60

BG_COLOR = (180, 180, 180)
PANEL_COLOR = (255, 255, 255)
PANEL_BORDER_RADIUS = 18

PLACEHOLDER_COLOR = (230, 230, 230)

# Where your icon PNG files live (update to your path)
ICON_BASE_PATH = "/Users/janet/Downloads/pfad/HK-rainfall-visualiser-/image"

# Optional: path to a TTF/OTF font file (Google Sans or another). If None or not found, system font used.
# Example: "/Users/janet/Downloads/fonts/GoogleSans-Regular.ttf"
FONT_PATH = None  # set to your font file path if you have one

# Duration (seconds) that the clicked color variant remains active
TEMP_VARIANT_DURATION = 0.35

FPS_CLOCK = pygame.time.Clock()

# ---------- Helpers ----------
def rounded_rect(surface, rect, color, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)


def point_in_rect(pt, rect):
    return rect.collidepoint(pt)



# ---------- Icon ----------


# ---------- Font loader ----------
def load_font(default_size):
    """
    Try to load custom font file (FONT_PATH). If not available, return a SysFont fallback.
    """
    if FONT_PATH:
        try:
            return pygame.font.Font(FONT_PATH, default_size)
        except Exception as e:
            print("Failed to load custom font at", FONT_PATH, "->", e)
    # fallback: try to use Google Sans family name (likely not installed), else default
    try:
        return pygame.font.SysFont("Google Sans", default_size)
    except Exception:
        return pygame.font.SysFont(None, default_size)

# ---------- Main ----------
def main():

    # Initialize pygame and display before creating any ImageButton
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("UI: temporary icon variant + custom font")
    font = load_font(20)

    # Create three buttons: start, stop, reload (after pygame is initialized)

    # Load base button image and icons

    button_on = pygame.image.load(os.path.join(ICON_BASE_PATH, "button_on.png")).convert_alpha()
    button_off = pygame.image.load(os.path.join(ICON_BASE_PATH, "button_off.png")).convert_alpha()
    icon_start_black = pygame.image.load(os.path.join(ICON_BASE_PATH, "start_black.png")).convert_alpha()
    icon_start_green = pygame.image.load(os.path.join(ICON_BASE_PATH, "start_green.png")).convert_alpha()
    icon_stop_black = pygame.image.load(os.path.join(ICON_BASE_PATH, "stop_black.png")).convert_alpha()
    icon_stop_red = pygame.image.load(os.path.join(ICON_BASE_PATH, "stop_red.png")).convert_alpha()
    icon_reload_black = pygame.image.load(os.path.join(ICON_BASE_PATH, "reload_black.png")).convert_alpha()

    class OverlayButton:
        def __init__(self, rect, icon_normal, icon_pressed=None, callback=None):
            self.rect = pygame.Rect(rect)
            self.icon_normal = icon_normal
            self.icon_pressed = icon_pressed if icon_pressed is not None else icon_normal
            self.down = False
            self.callback = callback

        def draw(self, surface):
            # Draw button background (on or off)
            bg = button_off if self.down else button_on
            bg_scaled = pygame.transform.smoothscale(bg, (self.rect.width, self.rect.height))
            surface.blit(bg_scaled, (self.rect.x, self.rect.y))
            # Draw icon centered, keep original aspect ratio, fit within 40% of button size
            icon = self.icon_pressed if self.down else self.icon_normal
            max_w = int(self.rect.width * 0.4)
            max_h = int(self.rect.height * 0.4)
            iw, ih = icon.get_width(), icon.get_height()
            scale = min(max_w / iw, max_h / ih, 1.0)
            new_w = int(iw * scale)
            new_h = int(ih * scale)
            icon_scaled = pygame.transform.smoothscale(icon, (new_w, new_h))
            icon_x = self.rect.x + (self.rect.width - new_w) // 2
            icon_y = self.rect.y + (self.rect.height - new_h) // 2
            surface.blit(icon_scaled, (icon_x, icon_y))

        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.down = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.down and self.rect.collidepoint(event.pos):
                    if self.callback:
                        self.callback(self)
                self.down = False

    btn_start = OverlayButton((0,0,80,80), icon_start_black, icon_start_green)
    btn_stop = OverlayButton((0,0,80,80), icon_stop_black, icon_stop_red)
    btn_reload = OverlayButton((0,0,80,80), icon_reload_black)

    def on_start(btn):
        print("Start button clicked")
    def on_stop(btn):
        print("Stop button clicked")
    def on_reload(btn):
        print("Reload button clicked")

    btn_start.callback = on_start
    btn_stop.callback = on_stop
    btn_reload.callback = on_reload

    def layout(window_w, window_h):
        margin = int(min(window_w, window_h) * 0.03)
        inner_rect = pygame.Rect(margin, margin, window_w - 2*margin, window_h - 2*margin)
        return inner_rect


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                pass
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            btn_start.handle_event(event)
            btn_stop.handle_event(event)
            btn_reload.handle_event(event)

        w, h = screen.get_size()
        inner = layout(w, h)

        # Button layout (bottom right) -- must be after 'inner' is defined
        btn_size = max(48, int(min(inner.width, inner.height) * 0.08))
        spacing = int(btn_size * 0.25)
        total_width = btn_size * 3 + spacing * 2
        base_x = inner.right - total_width - int(inner.width * 0.035)
        base_y = inner.bottom - btn_size - int(inner.height * 0.04)

        btn_start.rect = pygame.Rect(base_x, base_y, btn_size, btn_size)
        btn_stop.rect = pygame.Rect(base_x + btn_size + spacing, base_y, btn_size, btn_size)
        btn_reload.rect = pygame.Rect(base_x + (btn_size + spacing) * 2, base_y, btn_size, btn_size)

        # placeholder rect
        ph_w = int(inner.width * 0.32)
        ph_h = int(inner.height * 0.18)
        ph_x = inner.x + int(inner.width * 0.04)
        ph_y = inner.y + inner.height - ph_h - int(inner.height * 0.04)
        placeholder_rect = pygame.Rect(ph_x, ph_y, ph_w, ph_h)

        # Draw background and panels
        screen.fill(BG_COLOR)
        rounded_rect(screen, inner, PANEL_COLOR, PANEL_BORDER_RADIUS)
        rounded_rect(screen, placeholder_rect, PLACEHOLDER_COLOR, radius=12)

        # Draw the three image buttons
        btn_start.draw(screen)
        btn_stop.draw(screen)
        btn_reload.draw(screen)

        pygame.display.flip()
        FPS_CLOCK.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()