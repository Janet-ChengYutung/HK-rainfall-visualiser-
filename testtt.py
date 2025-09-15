"""
ui_with_png_buttons.py

Pygame 範例：使用外部 PNG 圖示放到按鈕中間，並依按鈕點擊改變圖示或顏色。
- 圖檔目錄（範例）： /Users/janet/Downloads/pfad/HK-rainfall-visualiser-
- 範例檔名（不含副檔名）： start_black, start_green, start_red,
                              stop_black, stop_green, stop_red,
                              reload_black
- 若某圖檔找不到，程式會自動退回繪製內建向量圖示以免崩潰。
"""

import pygame
import pygame.gfxdraw
import sys
import math
import os

# ---------- Configuration ----------
WIDTH, HEIGHT = 1280, 720
FPS = 60

BG_COLOR = (180, 180, 180)
PANEL_COLOR = (255, 255, 255)
PANEL_BORDER_RADIUS = 18

PLACEHOLDER_COLOR = (230, 230, 230)
BUTTON_COLOR = (242, 242, 242)
BUTTON_HOVER = (225, 225, 225)
BUTTON_DOWN = (205, 205, 205)
ICON_COLOR = (32, 32, 32)
SHADOW_ALPHA = 36

# ---------- Your icon files settings ----------
# NOTE: Modify this base path if needed.
ICON_BASE_PATH = "/Users/janet/Downloads/pfad/HK-rainfall-visualiser-"
# NOTE: The code will append suffixes and ".png" to load specific images.
# Expected file examples (without extension): start_black.png, start_green.png, start_red.png, stop_black.png, stop_green.png, stop_red.png, reload_black.png

FPS_CLOCK = pygame.time.Clock()

# ---------- Helpers ----------
def rounded_rect(surface, rect, color, radius):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def draw_shadow(surface, rect, radius, offset=(4,4), alpha=40):
    sw = rect.width + abs(offset[0]) + 8
    sh = rect.height + abs(offset[1]) + 8
    shadow_surf = pygame.Surface((sw, sh), pygame.SRCALPHA)
    shadow_surf.fill((0,0,0,0))
    srect = pygame.Rect(4, 4, rect.width, rect.height)
    pygame.draw.rect(shadow_surf, (0,0,0,alpha), srect, border_radius=radius)
    surface.blit(shadow_surf, (rect.x + offset[0] - 4, rect.y + offset[1] - 4))

def point_in_rect(pt, rect):
    return rect.collidepoint(pt)

# ---------- Icon Loader ----------
class IconSet:
    """
    Load PNG icons for a button. Each IconSet holds multiple variants (e.g. black, green, red).
    If some images are missing, entries will be None.
    """
    def __init__(self, base_name):
        # base_name example: "start" or "stop" or "reload"
        self.base_name = base_name
        # convention: variants we expect
        self.variants = {
            "black": None,
            "green": None,
            "red": None
        }
        # reload may only have black; it's fine if others are None
        self.load_images()

    def load_images(self):
        for key in list(self.variants.keys()):
            filename = f"{self.base_name}_{key}.png"
            fullpath = os.path.join(ICON_BASE_PATH, filename)
            try:
                img = pygame.image.load(fullpath).convert_alpha()
                self.variants[key] = img
                # print("Loaded icon:", fullpath)
            except Exception as e:
                # image not found or load error -> leave as None, fallback will be used
                # print("Icon not found (will fallback):", fullpath, "->", e)
                self.variants[key] = None

    def get(self, variant):
        return self.variants.get(variant, None)

# ---------- Button Class using external icons ----------
class RoundedButton:
    def __init__(self, rect, role, iconset=None, radius=10):
        """
        role: a semantic role string, e.g. "start" (will toggle green), "stop" (will toggle red), "reload" (stays black)
        iconset: IconSet instance corresponding to this button role (may be None)
        """
        self.rect = pygame.Rect(rect)
        self.role = role  # "start" / "stop" / "reload"
        self.iconset = iconset
        self.radius = radius
        self.hover = False
        self.down = False
        # state: which variant to show; default "black"
        self.state_variant = "black"
        self.callback = None

    def set_state_variant(self, var):
        # var should be "black", "green", "red", etc.
        self.state_variant = var

    def draw_icon_with_png(self, surface):
        """
        NOTE: This function is responsible for placing the PNG icon centered in the button.
        Behavior:
        - If an appropriate PNG (matching current state variant) exists, scale it to fit within
          the icon area (keeping aspect ratio) and blit it centered.
        - If PNG not available, fall back to vector drawing (draw_icon_vector).
        """
        if self.iconset is None:
            # no iconset provided -> fallback
            self.draw_icon_vector(surface)
            return

        # Try to get the image for the current variant
        img = self.iconset.get(self.state_variant)
        if img is None:
            # fallback to black if current variant missing
            img = self.iconset.get("black")

        if img is None:
            # still None -> draw vector fallback
            self.draw_icon_vector(surface)
            return

        # Calculate area to place icon: keep padding so icon doesn't touch rounded corners
        pad = max(2, int(self.rect.width * 0.18))
        max_w = self.rect.width - pad*2
        max_h = self.rect.height - pad*2

        # Scale the image to fit in (max_w, max_h) while preserving aspect ratio
        iw, ih = img.get_size()
        scale = min(max_w / iw, max_h / ih, 1.0)  # don't upscale beyond original size; change to >1 to allow upscaling
        target_w = int(round(iw * scale))
        target_h = int(round(ih * scale))
        img_scaled = pygame.transform.smoothscale(img, (target_w, target_h))

        # Compute centered position
        dest_x = self.rect.x + (self.rect.width - target_w)//2
        dest_y = self.rect.y + (self.rect.height - target_h)//2

        surface.blit(img_scaled, (dest_x, dest_y))

    def draw_icon_vector(self, surface):
        """
        Fallback vector drawing (simpler shapes). This is used if PNG not found.
        """
        icon_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pad = max(2, int(self.rect.width * 0.18))
        inner_w = self.rect.width - pad*2
        inner_h = self.rect.height - pad*2
        cx = pad + inner_w/2.0
        cy = pad + inner_h/2.0

        if self.role == "start":
            # play triangle
            tri_w = inner_w * 0.58
            tri_h = inner_h * 0.62
            p1 = (cx - tri_w/2.0, cy - tri_h/2.0)
            p2 = (cx - tri_w/2.0, cy + tri_h/2.0)
            p3 = (cx + tri_w/2.0, cy)
            pts = [(int(round(x)), int(round(y))) for (x,y) in (p1,p2,p3)]
            pygame.gfxdraw.filled_polygon(icon_surf, pts, ICON_COLOR)
            pygame.gfxdraw.aapolygon(icon_surf, pts, ICON_COLOR)

        elif self.role == "stop":
            # stop: small filled square
            s = int(min(inner_w, inner_h) * 0.5)
            r = pygame.Rect(int(cx - s/2), int(cy - s/2), s, s)
            pygame.gfxdraw.box(icon_surf, r, ICON_COLOR)

        elif self.role == "reload":
            # simple circular arrow using lines
            radius = min(inner_w, inner_h) * 0.38
            pygame.gfxdraw.arc(icon_surf, int(cx), int(cy), int(radius), -160, 100, ICON_COLOR)
            # small arrowhead
            ae = math.radians(100)
            ax = int(cx + radius * math.cos(ae))
            ay = int(cy + radius * math.sin(ae))
            tip = (ax + 6, ay)
            left = (ax - 2, ay - 6)
            right = (ax - 2, ay + 6)
            tri = [(int(tip[0]), int(tip[1])), (int(left[0]), int(left[1])), (int(right[0]), int(right[1]))]
            pygame.gfxdraw.filled_polygon(icon_surf, tri, ICON_COLOR)

        surface.blit(icon_surf, (self.rect.x, self.rect.y))

    def draw(self, surface):
        # shadow
        draw_shadow(surface, self.rect, self.radius, offset=(3,3), alpha=SHADOW_ALPHA)
        # background depending on state
        color = BUTTON_COLOR
        if self.down:
            color = BUTTON_DOWN
        elif self.hover:
            color = BUTTON_HOVER
        rounded_rect(surface, self.rect, color, self.radius)

        # Draw PNG icon centered (main functionality)
        self.draw_icon_with_png(surface)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = point_in_rect(event.pos, self.rect)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if point_in_rect(event.pos, self.rect):
                self.down = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.down and point_in_rect(event.pos, self.rect):
                # Click action: change state_variant based on role
                # - start: toggle to green when clicked (show start_green)
                # - stop: toggle to red when clicked (show stop_red)
                # - reload: no color change (stays black)
                if self.role == "start":
                    # toggle behavior: if currently green -> back to black, else set green
                    if self.state_variant == "green":
                        self.state_variant = "black"
                    else:
                        self.state_variant = "green"
                elif self.role == "stop":
                    if self.state_variant == "red":
                        self.state_variant = "black"
                    else:
                        self.state_variant = "red"
                elif self.role == "reload":
                    self.state_variant = "black"
                # call callback if set
                if self.callback:
                    self.callback(self)
            self.down = False

# ---------- Main ----------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("UI with PNG button icons")
    font = pygame.font.SysFont(None, 20)

    # Prepare IconSets for each button role
    # NOTE: This is the part "responsible for loading PNG icons from your folder".
    # You can change names here if your files differ.
    start_icons = IconSet("start")
    stop_icons = IconSet("stop")
    reload_icons = IconSet("reload")

    def layout(window_w, window_h):
        margin = int(min(window_w, window_h) * 0.03)
        inner_rect = pygame.Rect(margin, margin, window_w - 2*margin, window_h - 2*margin)
        return inner_rect

    # Create buttons and attach their IconSets
    buttons = []
    # Layout will be updated each frame, rects will be set later
    btn_start = RoundedButton((0,0,64,64), role="start", iconset=start_icons, radius=10)
    btn_stop = RoundedButton((0,0,64,64), role="stop", iconset=stop_icons, radius=10)
    btn_reload = RoundedButton((0,0,64,64), role="reload", iconset=reload_icons, radius=10)
    buttons = [btn_start, btn_stop, btn_reload]

    def on_button(btn):
        print("Button clicked:", btn.role, "state_variant:", btn.state_variant)

    for b in buttons:
        b.callback = on_button

    running = True
    while running:
        w, h = screen.get_size()
        inner = layout(w, h)

        # placeholder rectangle bottom-left
        ph_w = int(inner.width * 0.32)
        ph_h = int(inner.height * 0.18)
        ph_x = inner.x + int(inner.width * 0.04)
        ph_y = inner.y + inner.height - ph_h - int(inner.height * 0.04)
        placeholder_rect = pygame.Rect(ph_x, ph_y, ph_w, ph_h)

        # buttons layout bottom-right
        btn_size = max(48, int(min(inner.width, inner.height) * 0.06))
        btn_spacing = int(btn_size * 0.5)
        total_btn_width = btn_size * len(buttons) + btn_spacing * (len(buttons)-1)
        br_x = inner.x + inner.width - total_btn_width - int(inner.width * 0.035)
        br_y = inner.y + inner.height - btn_size - int(inner.height * 0.04)

        # set rects for buttons
        for i, b in enumerate(buttons):
            b.rect = pygame.Rect(br_x + i*(btn_size + btn_spacing), br_y, btn_size, btn_size)
            b.radius = int(btn_size * 0.18)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                pass
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            for b in buttons:
                b.handle_event(event)

        # Draw UI
        screen.fill(BG_COLOR)
        inner_shadow_rect = pygame.Rect(inner.x, inner.y, inner.width, inner.height)
        draw_shadow(screen, inner_shadow_rect, PANEL_BORDER_RADIUS, offset=(6,6), alpha=35)
        rounded_rect(screen, inner, PANEL_COLOR, PANEL_BORDER_RADIUS)

        draw_shadow(screen, placeholder_rect, 12, offset=(3,3), alpha=20)
        rounded_rect(screen, placeholder_rect, PLACEHOLDER_COLOR, radius=12)

        for b in buttons:
            b.draw(screen)

        # Demo labels
        label = font.render("Preview / content area", True, (120,120,120))
        screen.blit(label, (inner.x + 16, inner.y + 12))
        small = font.render("placeholder", True, (120,120,120))
        screen.blit(small, (placeholder_rect.x + 12, placeholder_rect.y + 10))

        pygame.display.flip()
        FPS_CLOCK.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()