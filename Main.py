import pygame
import pygame.gfxdraw
import sys
import math
import os
import time
import xml.etree.ElementTree as ET

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

# ---------- TSX Background Loader ----------
class TSXBackground:
    def __init__(self, tsx_file_path):
        """Load a TSX tileset file for use as a background."""
        self.tsx_path = tsx_file_path
        self.background_image = None
        self.tile_width = 0
        self.tile_height = 0
        self.image_width = 0
        self.image_height = 0
        self.load_tsx()
    
    def load_tsx(self):
        """Parse the TSX file and load the associated image."""
        try:
            if not os.path.exists(self.tsx_path):
                print(f"TSX file not found: {self.tsx_path}")
                return False
            
            # Parse the TSX XML file
            tree = ET.parse(self.tsx_path)
            root = tree.getroot()
            
            # Get tileset properties
            self.tile_width = int(root.get('tilewidth', 32))
            self.tile_height = int(root.get('tileheight', 32))
            
            # Find the image element
            image_elem = root.find('image')
            if image_elem is not None:
                image_source = image_elem.get('source')
                self.image_width = int(image_elem.get('width', 0))
                self.image_height = int(image_elem.get('height', 0))
                
                # Resolve image path relative to TSX file
                tsx_dir = os.path.dirname(self.tsx_path)
                image_path = os.path.join(tsx_dir, image_source)
                
                if os.path.exists(image_path):
                    self.background_image = pygame.image.load(image_path).convert()
                    print(f"Loaded TSX background: {image_path}")
                    return True
                else:
                    print(f"TSX image not found: {image_path}")
                    return False
            else:
                print("No image element found in TSX file")
                return False
                    
        except Exception as e:
            print(f"Error loading TSX file: {e}")
            return False
    
    def draw(self, surface, x=0, y=0, scale=None):
        """Draw the background image on the surface."""
        if self.background_image:
            if scale:
                # Scale the image to fit the surface or specified dimensions
                scaled_image = pygame.transform.scale(self.background_image, scale)
                surface.blit(scaled_image, (x, y))
            else:
                surface.blit(self.background_image, (x, y))
    
    def is_loaded(self):
        """Check if the TSX background was successfully loaded."""
        return self.background_image is not None

# Simple Pygame demo: 3 image buttons (start, stop, reload) with color change on press.

# ---------- Configuration ----------
WIDTH, HEIGHT = 1280, 720
FPS = 60

BG_COLOR = (180, 180, 180)
PANEL_COLOR = (255, 255, 255)
PANEL_BORDER_RADIUS = 18

PLACEHOLDER_COLOR = (230, 230, 230)

# Where your icon PNG files live (update to your path)
ICON_BASE_PATH = os.path.join(os.path.dirname(__file__), "image")

# Optional: path to a TSX background file (Tiled tileset format)
TSX_BACKGROUND_PATH = os.path.join(os.path.dirname(__file__), "sample_background.tsx")

# Optional: path to a TTF/OTF font file (Google Sans or another). If None or not found, system font used.
# Example: "/Users/janet/Downloads/fonts/GoogleSans-Regular.ttf"
FONT_PATH = None  # set to your font file path if you have one

# Duration (seconds) that the clicked color variant remains active
TEMP_VARIANT_DURATION = 0.35

FPS_CLOCK = pygame.time.Clock()

# (removed unused point_in_rect)
# ---------- Icon ----------



# ---------- Main ----------
def main():

    # Initialize pygame and display before creating any ImageButton
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("UI: temporary icon variant + custom font")

    # Load TSX background if available
    tsx_background = None
    if os.path.exists(TSX_BACKGROUND_PATH):
        tsx_background = TSXBackground(TSX_BACKGROUND_PATH)
        if tsx_background.is_loaded():
            print(f"TSX background loaded successfully from: {TSX_BACKGROUND_PATH}")
        else:
            print("Failed to load TSX background, using default background color")
    else:
        print(f"TSX background file not found: {TSX_BACKGROUND_PATH}")

    # Create three buttons: start, stop, reload (after pygame is initialized)

    # Load base button image and icons

    button_on = pygame.image.load(os.path.join(ICON_BASE_PATH, "button_on.png")).convert_alpha()
    button_off = pygame.image.load(os.path.join(ICON_BASE_PATH, "button_off.png")).convert_alpha()
    icon_start_black = pygame.image.load(os.path.join(ICON_BASE_PATH, "start_black.png")).convert_alpha()
    icon_start_green = pygame.image.load(os.path.join(ICON_BASE_PATH, "start_green.png")).convert_alpha()
    icon_stop_black = pygame.image.load(os.path.join(ICON_BASE_PATH, "stop_black.png")).convert_alpha()
    icon_stop_red = pygame.image.load(os.path.join(ICON_BASE_PATH, "stop_red.png")).convert_alpha()
    icon_reload_black = pygame.image.load(os.path.join(ICON_BASE_PATH, "reload_black.png")).convert_alpha()
    # Chart icons for the new button (chart_off -> chart_on when pressed)
    icon_chart_off = pygame.image.load(os.path.join(ICON_BASE_PATH, "chart_off.png")).convert_alpha()
    icon_chart_on = pygame.image.load(os.path.join(ICON_BASE_PATH, "chart_on.png")).convert_alpha()

    # Load Google Sans Code font if available, otherwise use default system font
    font_path = os.path.join(os.path.dirname(__file__), "GoogleSansCode-VariableFont_wght.ttf")
    if os.path.exists(font_path):
        try:
            UI_FONT = pygame.font.Font(font_path, 20)
        except Exception:
            UI_FONT = pygame.font.SysFont(None, 20)
    else:
        UI_FONT = pygame.font.SysFont(None, 20)

    # Year slider widget (minimalist)
    class YearSlider:
        def __init__(self, rect, year_min=1884, year_max=2025, initial=None):
            self.rect = pygame.Rect(rect)
            self.year_min = year_min
            self.year_max = year_max
            self.range = year_max - year_min
            self.year = initial if initial is not None else year_max
            self.dragging = False

        def year_to_pos(self, year):
            t = (year - self.year_min) / max(1, self.range)
            return int(self.rect.x + 8 + t * (self.rect.width - 16))

        def pos_to_year(self, x):
            t = (x - (self.rect.x + 8)) / max(1, (self.rect.width - 16))
            year = int(round(self.year_min + t * self.range))
            year = max(self.year_min, min(self.year_max, year))
            # remove choice for 1940-1946 by snapping to nearest allowed year
            if 1940 <= year <= 1946:
                # choose nearest of 1939 or 1947
                low = 1939
                high = 1947
                # clamp to bounds
                if low < self.year_min:
                    return high
                if high > self.year_max:
                    return low
                if (year - low) <= (high - year):
                    return low
                else:
                    return high
            return year

        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.dragging = True
                    self.year = self.pos_to_year(event.pos[0])
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    self.year = self.pos_to_year(event.pos[0])
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.dragging:
                    self.dragging = False

        def draw(self, surface, font):
            # bar background
            bar_h = 8
            bar_rect = pygame.Rect(self.rect.x, self.rect.y + (self.rect.height - bar_h)//2, self.rect.width, bar_h)
            pygame.draw.rect(surface, (200,200,200), bar_rect, border_radius=4)
            # fill upto current year
            pos = self.year_to_pos(self.year)
            fill_rect = pygame.Rect(bar_rect.x+4, bar_rect.y, pos - (bar_rect.x+4), bar_rect.height)
            pygame.draw.rect(surface, (120,160,255), fill_rect, border_radius=4)
            # thumb
            thumb_r = 10
            pygame.draw.circle(surface, (255,255,255), (pos, bar_rect.centery), thumb_r)
            pygame.draw.circle(surface, (100,120,140), (pos, bar_rect.centery), thumb_r, 2)
            # year label above bar
            year_surf = font.render(str(self.year), True, (20,20,20))
            ys = year_surf.get_rect(center=(pos, bar_rect.y - 14))
            surface.blit(year_surf, ys)

    # instantiate year slider and place it bottom-center
    slider_w = int(WIDTH * 0.4)
    slider_h = 40
    slider_x = (WIDTH - slider_w) // 2
    slider_y = HEIGHT - slider_h - 24
    year_slider = YearSlider((slider_x, slider_y, slider_w, slider_h), 1884, 2025, 2025)

    class OverlayButton:
        def __init__(self, rect, icon_normal, icon_pressed=None, callback=None, toggle=False):
            self.rect = pygame.Rect(rect)
            self.icon_normal = icon_normal
            self.icon_pressed = icon_pressed if icon_pressed is not None else icon_normal
            self.down = False
            self.callback = callback
            # whether this button toggles (sticky) on click
            self.toggle = toggle
            # persistent toggle state for toggle buttons
            self.toggled = False
            # default flag for reload button sizing; can be toggled externally
            self.is_reload = False

        def draw(self, surface):
            # Determine the effective pressed state: for toggle buttons use persistent
            # `toggled`, otherwise use transient `down`.
            effective_down = self.toggled if self.toggle else self.down
            # Draw button background (on or off)
            bg = button_off if effective_down else button_on
            # If pressed (either transient or persistent), draw the background slightly smaller and 3px higher.
            if effective_down:
                # shrink by a few pixels so the change is subtle
                new_w = max(1, self.rect.width - 6)
                new_h = max(1, self.rect.height - 6)
                bg_scaled = pygame.transform.smoothscale(bg, (new_w, new_h))
                bg_x = self.rect.x + (self.rect.width - new_w) // 2
                bg_y = self.rect.y + (self.rect.height - new_h) // 2 - 3  # raise by 3px
                surface.blit(bg_scaled, (bg_x, bg_y))
            else:
                bg_scaled = pygame.transform.smoothscale(bg, (self.rect.width, self.rect.height))
                surface.blit(bg_scaled, (self.rect.x, self.rect.y))
            # Draw icon centered, keep original aspect ratio, fit within 40% of button size
            icon = self.icon_pressed if effective_down else self.icon_normal
            # Make reload icon slightly larger (45% of button size), others 40%
            if getattr(self, 'is_reload', False):
                icon_scale_factor = 0.45
            else:
                icon_scale_factor = 0.4
            max_w = int(self.rect.width * icon_scale_factor)
            max_h = int(self.rect.height * icon_scale_factor)
            iw, ih = icon.get_width(), icon.get_height()
            scale = min(max_w / iw, max_h / ih, 1.0)
            new_w = int(iw * scale)
            new_h = int(ih * scale)
            icon_scaled = pygame.transform.smoothscale(icon, (new_w, new_h))
            # Keep the icon centered in the original button rect.
            # When pressed, move the icon 3px lower to give a pressed-in effect.
            icon_x = self.rect.x + (self.rect.width - new_w) // 2
            # Default: unpressed icons should be 3px higher
            icon_y = self.rect.y + (self.rect.height - new_h) // 2 - 3
            # When pressed (either transient or persistent), move the icon down 3px
            # (so for toggles the icon appears pressed while toggled on)
            if effective_down:
                icon_y += 3
            surface.blit(icon_scaled, (icon_x, icon_y))

        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    # show visual pressed state on mouse down for momentary and toggle buttons
                    self.down = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.down and self.rect.collidepoint(event.pos):
                    if self.toggle:
                        # flip persistent toggle state
                        self.toggled = not self.toggled
                        # align transient visual with persistent state
                        self.down = self.toggled
                    if self.callback:
                        self.callback(self)
                # clear transient pressed state for non-toggle buttons
                if not self.toggle:
                    self.down = False

    btn_start = OverlayButton((0,0,80,80), icon_start_black, icon_start_green)
    btn_stop = OverlayButton((0,0,80,80), icon_stop_black, icon_stop_red)
    btn_reload = OverlayButton((0,0,80,80), icon_reload_black)
    # New chart button placed above the reload button (toggle)
    btn_chart = OverlayButton((0,0,80,80), icon_chart_off, icon_chart_on, toggle=True)
    btn_reload.is_reload = True  # Mark this button as reload for larger icon


    def on_start(btn):
        print("Start button clicked")
    def on_stop(btn):
        print("Stop button clicked")
    def on_reload(btn):
        print("Reload button clicked")
    def on_chart(btn):
        # Chart button callback: kept for logging. Panel visibility is driven
        # directly by the button state in the main loop (pressed or toggled).
        print("Chart button clicked; toggled=" + str(btn.toggled) + ", down=" + str(btn.down))

    btn_start.callback = on_start
    btn_stop.callback = on_stop
    btn_reload.callback = on_reload
    btn_chart.callback = on_chart


    def layout(window_w, window_h):
        margin = int(min(window_w, window_h) * 0.03)
        return pygame.Rect(margin, margin, window_w - 2*margin, window_h - 2*margin)


    running = True
    # cache loaded yearly chart images to avoid repeated disk IO
    chart_image_cache = {}
    # chart drag-and-drop state
    chart_pos = None  # (x,y) where the chart is drawn; preserved across frames
    chart_dragging = False
    chart_drag_offset = (0, 0)
    last_chart_rect = None  # pygame.Rect of last drawn chart (for hit testing)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                pass
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            # --- chart drag handling (start/stop/drag) ---
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # start dragging if user clicked on the last drawn chart while it's visible
                if (btn_chart.toggled or btn_chart.down) and last_chart_rect is not None and last_chart_rect.collidepoint(event.pos):
                    chart_dragging = True
                    mx, my = event.pos
                    chart_drag_offset = (mx - last_chart_rect.x, my - last_chart_rect.y)
            elif event.type == pygame.MOUSEMOTION:
                if chart_dragging:
                    mx, my = event.pos
                    chart_pos = (int(mx - chart_drag_offset[0]), int(my - chart_drag_offset[1]))
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if chart_dragging:
                    chart_dragging = False
            btn_start.handle_event(event)
            btn_stop.handle_event(event)
            btn_reload.handle_event(event)
            btn_chart.handle_event(event)
            year_slider.handle_event(event)

        w, h = screen.get_size()
        inner = layout(w, h)
        btn_size = max(48, int(min(inner.width, inner.height) * 0.08))
        spacing = int(btn_size * 0.25)
        total_width = btn_size * 3 + spacing * 2
        base_x = inner.right - total_width - int(inner.width * 0.035)
        base_y = inner.bottom - btn_size - int(inner.height * 0.04)
        btn_start.rect = pygame.Rect(base_x, base_y, btn_size, btn_size)
        btn_stop.rect = pygame.Rect(base_x + btn_size + spacing, base_y, btn_size, btn_size)
        btn_reload.rect = pygame.Rect(base_x + (btn_size + spacing) * 2, base_y, btn_size, btn_size)
        # place chart button above the reload button
        btn_chart.rect = pygame.Rect(base_x + (btn_size + spacing) * 2, base_y - (btn_size + spacing), btn_size, btn_size)
        # Clear screen and draw background
        if tsx_background and tsx_background.is_loaded():
            # Use TSX background scaled to fit window
            w, h = pygame.display.get_surface().get_size()
            tsx_background.draw(screen, scale=(w, h))
        else:
            # Use default background color
            screen.fill(BG_COLOR)
        # Draw a rounded rectangle frame (panel) in the lower left. If a pre-rendered
        # chart for the selected year exists, size the panel to match the chart aspect
        # ratio while fitting within a maximum area.
        # Allow the chart to occupy a larger portion of the window so
        # high-resolution images are shown nearer to native resolution.
        # These fractions can be adjusted if you prefer a different max size.
        max_panel_w = int(w * 0.45)
        max_panel_h = int(h * 0.60)
        panel_x = int(w * 0.047)
        # default place near bottom with a small bottom margin
        bottom_margin = int(h * 0.04)
        # Show panel while the chart button is pressed (down) or toggled on
        if btn_chart.toggled or btn_chart.down:
            # look for pre-rendered chart image for the selected year
            chart_year = year_slider.year
            chart_path = os.path.join(os.path.dirname(__file__), 'rainfall_charts', f'rainfall_{chart_year}.png')
            img = None
            if chart_year in chart_image_cache:
                img = chart_image_cache[chart_year]
            else:
                if os.path.exists(chart_path):
                    try:
                        loaded = pygame.image.load(chart_path).convert_alpha()
                        chart_image_cache[chart_year] = loaded
                        img = loaded
                    except Exception:
                        img = None
            if img is not None:
                iw, ih = img.get_width(), img.get_height()
                # enlarge chart by 40% but ensure it fits inside max panel area
                enlarge_factor = 1.40
                scale = min(max_panel_w / (iw * enlarge_factor), max_panel_h / (ih * enlarge_factor), 1.0)
                chart_w = max(1, int(iw * scale * enlarge_factor))
                chart_h = max(1, int(ih * scale * enlarge_factor))
                panel_y = h - chart_h - bottom_margin
                # draw the chart image directly (no panel box), opaque (100% opacity)
                alpha = 255
                img_scaled = pygame.transform.smoothscale(img, (chart_w, chart_h)).convert_alpha()
                img_scaled.set_alpha(alpha)
                # if the user moved the chart, use chart_pos; otherwise default to panel origin
                if chart_pos is None:
                    surface_x = panel_x
                    surface_y = panel_y
                    chart_pos = (surface_x, surface_y)
                else:
                    surface_x, surface_y = chart_pos
                screen.blit(img_scaled, (surface_x, surface_y))
                # remember the rect so we can start dragging from it next frame
                last_chart_rect = pygame.Rect(int(surface_x), int(surface_y), chart_w, chart_h)
            else:
                # fallback to previous placeholder with max size
                panel_w = max_panel_w
                panel_h = max_panel_h
                panel_y = int(HEIGHT * 0.75)
                # semi-transparent rounded panel background for placeholder (50% opacity)
                alpha = int(255 * 0.5)
                radius = max(6, int(PANEL_BORDER_RADIUS * 1.2))
                panel_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
                pygame.draw.rect(panel_surf, (PANEL_COLOR[0], PANEL_COLOR[1], PANEL_COLOR[2], alpha), (0, 0, panel_w, panel_h), border_radius=radius)
                screen.blit(panel_surf, (panel_x, panel_y))
                # draw placeholder chart inside panel
                chart_margin = 12
                cx = panel_x + chart_margin
                cy = panel_y + chart_margin
                cw = panel_w - chart_margin*2
                ch = panel_h - chart_margin*2
                # background for chart area
                pygame.draw.rect(screen, (245,245,250), (cx, cy, cw, ch), border_radius=6)
                # axes
                ax_x = cx + 30
                ax_y = cy + ch - 24
                pygame.draw.line(screen, (180,180,180), (ax_x, cy+6), (ax_x, ax_y), 2)
                pygame.draw.line(screen, (180,180,180), (ax_x, ax_y), (cx+cw-8, ax_y), 2)
                # sample data generated from year (to vary visually)
                samples = 24
                pts = []
                seed = year_slider.year % 10
                for i in range(samples):
                    t = i / (samples-1)
                    x = ax_x + int(t * (cw - 48))
                    # simple wave + seed offset
                    yval = 0.5 + 0.4 * math.sin(2*math.pi*(t*3 + seed*0.13))
                    y = int(ax_y - yval * (ch - 48))
                    pts.append((x,y))
                if len(pts) > 1:
                    pygame.draw.lines(screen, (40,120,200), False, pts, 3)
                # label with the selected year
                label = UI_FONT.render(f"Year: {year_slider.year}", True, (40,40,40))
                screen.blit(label, (cx+6, cy+6))
        btn_start.draw(screen)
        btn_stop.draw(screen)
        btn_reload.draw(screen)
        btn_chart.draw(screen)
        # draw year slider on bottom center
        year_slider.draw(screen, UI_FONT)
        pygame.display.flip()
        FPS_CLOCK.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()