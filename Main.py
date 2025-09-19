import pygame
import pygame.gfxdraw
import sys
import math
import os
import time
# Safe stub for TSX background loader (project may provide a real loader elsewhere)
def create_tsx_background(path, w, h):
    return None

# optional animation module (animationtest) and rainfall loader (viewchart)
try:
    import animationtest
except Exception:
    animationtest = None
try:
    from viewchart import load_rainfall_data
except Exception:
    load_rainfall_data = None

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

# Path to TSX background file (set to None to disable TSX background)
TSX_BACKGROUND_PATH = os.path.join(os.path.dirname(__file__), "animation.tsx")  # or None to use default solid color background

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
            # smaller font for year label above the slider
            # Prefer a system font that contains digit glyphs to avoid missing-glyph boxes.
            preferred = ['arialunicode', 'arial', 'helvetica', 'timesnewroman']
            found = None
            available = {f.lower() for f in pygame.font.get_fonts()}
            for p in preferred:
                if p in available:
                    found = p
                    break
            if found:
                YEAR_FONT = pygame.font.SysFont(found, 14)
            else:
                # fallback to packaged font if system fonts don't contain digits
                YEAR_FONT = pygame.font.Font(font_path, 14)
        except Exception:
            UI_FONT = pygame.font.SysFont(None, 20)
            YEAR_FONT = pygame.font.SysFont(None, 14)
    else:
        UI_FONT = pygame.font.SysFont(None, 20)
        YEAR_FONT = pygame.font.SysFont(None, 14)

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
            # year label above bar (use smaller YEAR_FONT if available)
            try:
                year_surf = YEAR_FONT.render(str(self.year), True, (255,255,255))
            except Exception:
                year_surf = font.render(str(self.year), True, (255,255,255))
            # place year label flush with the left end of the slider bar
            bg_margin = 6
            # left end x coordinate of the bar
            left_x = bar_rect.x
            # compute background rect positioned to the immediate left of the bar,
            # vertically centered with the bar
            bg_w = year_surf.get_width() + bg_margin*2
            bg_h = year_surf.get_height() + bg_margin*2
            gap = 6
            bg_x = left_x - bg_w - gap
            bg_y = bar_rect.centery - (bg_h // 2)
            bg_rect = pygame.Rect(bg_x, bg_y, bg_w, bg_h)
            pygame.draw.rect(surface, (0,0,0), bg_rect)
            # blit year text inside the square
            text_x = bg_x + bg_margin
            text_y = bg_y + bg_margin
            surface.blit(year_surf, (text_x, text_y))
            # blit year text inside the black square with margin
            text_x = bg_x + bg_margin
            text_y = bg_y + bg_margin
            surface.blit(year_surf, (text_x, text_y))

    # instantiate year slider and place it bottom-center
    slider_w = int(WIDTH * 0.4)
    slider_h = 40
    slider_x = (WIDTH - slider_w) // 2
    slider_y = HEIGHT - slider_h - 24
    year_slider = YearSlider((slider_x, slider_y, slider_w, slider_h), 1884, 2025, 2025)

    # Animation background state (if animationtest is available)
    animation_enabled = animationtest is not None
    anim_frame_time = 0.0
    anim_font = None
    anim_surface = None
    anim_char_w = anim_char_h = None
    rainfall_by_year = None
    # try loading monthlyElement.xml via viewchart if available
    try:
        if load_rainfall_data is not None:
            xml_path = os.path.join(os.path.dirname(__file__), 'monthlyElement.xml')
            if os.path.exists(xml_path):
                years_list, rainfall_list = load_rainfall_data(xml_path)
                rainfall_by_year = {str(y): vals for y, vals in zip(years_list, rainfall_list)}
    except Exception:
        rainfall_by_year = None
    # Audio: load rain sound (best-effort) and setup per-month volume control
    rain_sound_path = os.path.join(os.path.dirname(__file__), 'rain_sound.mp3')
    music_available = False
    # compute per-year min/max monthly values for normalization
    per_year_month_minmax = {}
    try:
        if rainfall_by_year:
            for y, vals in rainfall_by_year.items():
                if vals:
                    per_year_month_minmax[y] = (min(vals), max(vals))
    except Exception:
        per_year_month_minmax = {}
    try:
        pygame.mixer.init()
        if os.path.exists(rain_sound_path):
            try:
                pygame.mixer.music.load(rain_sound_path)
                pygame.mixer.music.play(-1)
                music_available = True
            except Exception:
                music_available = False
        else:
            music_available = False
    except Exception:
        music_available = False
    

    class OverlayButton:
        def __init__(self, rect, icon_normal, icon_pressed=None, callback=None, toggle=False):
            self.rect = pygame.Rect(rect)
            self.icon_normal = icon_normal
            self.icon_pressed = icon_pressed if icon_pressed is not None else icon_normal
            self.down = False
            self.callback = callback
            # whether this button toggles (sticky) on click
            self.toggle = toggle
            # whether the button is enabled (clickable)
            self.enabled = True
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
            # If disabled, draw a dimmed background/icon to indicate locked state
            if not getattr(self, 'enabled', True):
                # draw a slightly darker overlay on top of button background
                overlay = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
                overlay.fill((0,0,0,120))
                surface.blit(overlay, (self.rect.x, self.rect.y))

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
            # Ignore interactions when disabled
            if not getattr(self, 'enabled', True):
                return
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

    # Make start/stop toggle buttons so their visual state reflects running/stopped
    btn_start = OverlayButton((0,0,80,80), icon_start_black, icon_start_green, toggle=True)
    btn_stop = OverlayButton((0,0,80,80), icon_stop_black, icon_stop_red, toggle=True)
    # reload is momentary
    btn_reload = OverlayButton((0,0,80,80), icon_reload_black)
    # New chart button placed above the reload button (toggle)
    btn_chart = OverlayButton((0,0,80,80), icon_chart_off, icon_chart_on, toggle=True)
    btn_reload.is_reload = True  # Mark this button as reload for larger icon


    def on_start(btn):
        # start the animation
        try:
            nonlocal animation_enabled, btn_start, btn_stop, btn_chart
        except SyntaxError:
            pass
        animation_enabled = True
        # update visual toggles
        btn_start.toggled = True
        btn_stop.toggled = False
        # enable chart button (unlock)
        try:
            btn_chart.enabled = True
        except Exception:
            pass
        # resume music (best-effort)
        try:
            pygame.mixer.music.unpause()
        except Exception:
            pass
        print("Start button clicked; animation enabled")

    def on_stop(btn):
        # stop the animation (pause)
        try:
            nonlocal animation_enabled, btn_start, btn_stop, btn_chart, chart_pos, chart_dragging, last_chart_rect
        except SyntaxError:
            pass
        animation_enabled = False
        btn_start.toggled = False
        btn_stop.toggled = True
        # Disable (lock) the chart button and clear transient chart state
        try:
            btn_chart.enabled = False
            btn_chart.toggled = False
            btn_chart.down = False
            chart_pos = None
            chart_dragging = False
            last_chart_rect = None
        except Exception:
            pass
        # pause music (best-effort)
        try:
            pygame.mixer.music.pause()
        except Exception:
            pass
        print("Stop button clicked; animation disabled and chart locked/closed")

    def on_reload(btn):
        # reset animation state so it restarts from initial frame
        try:
            nonlocal anim_frame_time, anim_surface, anim_font, anim_char_w, anim_char_h, rainfall_by_year
        except SyntaxError:
            pass
        anim_frame_time = 0.0
        anim_surface = None
        anim_font = None
        anim_char_w = anim_char_h = None
        # attempt to re-load rainfall data if loader is available
        try:
            if load_rainfall_data is not None:
                xml_path = os.path.join(os.path.dirname(__file__), 'monthlyElement.xml')
                if os.path.exists(xml_path):
                    years_list, rainfall_list = load_rainfall_data(xml_path)
                    rainfall_by_year = {str(y): vals for y, vals in zip(years_list, rainfall_list)}
        except Exception:
            rainfall_by_year = rainfall_by_year
        print("Reload button clicked; animation reset")
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
    # TSX background surface cache
    tsx_background_surface = None
    # cache last scaled animation frame so we can freeze it when paused
    last_anim_frame = None
    # music month cycling state: which month index (0..11) is currently driving volume
    music_month_index = 0
    # seconds per month step (controls how fast the music volume cycles through months)
    MUSIC_MONTH_STEP = 0.8
    music_month_time_acc = 0.0
    # smooth volume state
    MUSIC_VOLUME_SMOOTHING = 0.6  # smaller = slower smoothing (per-second rate); lower value gives longer fades
    current_music_volume = 0.35
    # chart drag-and-drop state
    chart_pos = None  # (x,y) where the chart is drawn; preserved across frames
    chart_dragging = False
    chart_drag_offset = (0, 0)
    last_chart_rect = None  # pygame.Rect of last drawn chart (for hit testing)
    
    # Load TSX background if specified
    if TSX_BACKGROUND_PATH and os.path.exists(TSX_BACKGROUND_PATH):
        print(f"Loading TSX background from: {TSX_BACKGROUND_PATH}")
        try:
            tsx_background_surface = create_tsx_background(TSX_BACKGROUND_PATH, WIDTH, HEIGHT)
            if tsx_background_surface:
                print("TSX background loaded successfully!")
            else:
                print("Failed to load TSX background, using default background")
        except Exception as e:
            print(f"Error loading TSX background: {e}")
    elif TSX_BACKGROUND_PATH:
        print(f"TSX background file not found: {TSX_BACKGROUND_PATH}")
    
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
        
        # Draw background - TSX background if available, otherwise animation or solid color
        if tsx_background_surface:
            # Scale TSX background to current window size if needed
            current_w, current_h = screen.get_size()
            if (current_w, current_h) != (WIDTH, HEIGHT):
                scaled_bg = pygame.transform.smoothscale(tsx_background_surface, (current_w, current_h))
                screen.blit(scaled_bg, (0, 0))
            else:
                screen.blit(tsx_background_surface, (0, 0))
        else:
            # update animation time
            if animation_enabled and animationtest is not None:
                now = time.time()
                # use FPS_CLOCK to compute dt for smoother timing
                dt = FPS_CLOCK.get_time() / 1000.0 if FPS_CLOCK else 1.0 / FPS
                anim_frame_time += dt
                # prepare font and surface on first use
                if anim_font is None:
                    monos = pygame.font.match_font('consolas, courier, monospace')
                    if monos:
                        anim_font = pygame.font.Font(monos, animationtest.FONT_SIZE)
                    else:
                        anim_font = pygame.font.SysFont('couriernew', animationtest.FONT_SIZE)
                    sample = anim_font.render('M', True, (255,255,255))
                    anim_char_w, anim_char_h = sample.get_size()
                    anim_surface = pygame.Surface((anim_char_w * animationtest.COLS + animationtest.PADDING*2,
                                                   anim_char_h * animationtest.ROWS + animationtest.PADDING*2))
                # choose rainfall data for selected year
                sel_year = str(year_slider.year)
                if rainfall_by_year and sel_year in rainfall_by_year:
                    data_for_year = rainfall_by_year[sel_year]
                else:
                    data_for_year = getattr(animationtest, 'RAIN_DATA', None)
                # Update music month timer and set volume based on monthly rainfall
                try:
                    if music_available and data_for_year:
                        # advance month time accumulator
                        music_month_time_acc += dt
                        while music_month_time_acc >= MUSIC_MONTH_STEP:
                            music_month_time_acc -= MUSIC_MONTH_STEP
                            music_month_index = (music_month_index + 1) % 12
                        # pick month index and value (wrap if data shorter)
                        if len(data_for_year) >= 12:
                            month_val = float(data_for_year[music_month_index % 12])
                        else:
                            # if data_for_year is a yearly mean or shorter, fallback to mean
                            try:
                                month_val = float(sum(data_for_year) / max(1, len(data_for_year)))
                            except Exception:
                                month_val = 0.0
                        # normalize month_val to 0..1 using per-year min/max if available
                        vol = 0.35
                        try:
                            if sel_year in per_year_month_minmax:
                                lo, hi = per_year_month_minmax[sel_year]
                                if hi > lo:
                                    t = (month_val - lo) / (hi - lo)
                                else:
                                    t = 0.0
                            else:
                                t = 0.0
                        except Exception:
                            t = 0.0
                        # curve and map to audible range
                        t = max(0.0, min(1.0, t))
                        target_vol = 0.05 + (t ** 0.9) * 0.95
                        # smooth toward target_vol using exponential smoothing
                        try:
                            alpha = 1.0 - math.exp(-MUSIC_VOLUME_SMOOTHING * dt)
                        except Exception:
                            alpha = 0.25
                        current_music_volume = (1.0 - alpha) * current_music_volume + alpha * target_vol
                        pygame.mixer.music.set_volume(max(0.0, min(1.0, current_music_volume)))
                except Exception:
                    pass
                # generate grid
                try:
                    grid = animationtest.generate_fluid_pattern(data_for_year, anim_frame_time,
                                                               cols=animationtest.COLS, rows=animationtest.ROWS,
                                                               speed_factor=animationtest.SPEED_FACTOR,
                                                               base_scale=animationtest.BASE_TIME_SCALE)
                except Exception:
                    grid = None
                # render to anim_surface
                if anim_surface and anim_char_w is not None and anim_char_h is not None:
                    anim_surface.fill(animationtest.BG_COLOR if hasattr(animationtest, 'BG_COLOR') else (0,0,0))
                    if grid:
                        for row_idx, row in enumerate(grid):
                            y = animationtest.PADDING + row_idx * anim_char_h
                            base = animationtest.row_base_color(row_idx, animationtest.ROWS,
                                                               top_whiten=animationtest.TOP_WHITEN_BIAS,
                                                               bottom_boost=animationtest.BOTTOM_WHITEN_BOOST)
                            for col_idx, (ch, norm) in enumerate(row):
                                col_mod = (math.sin((anim_frame_time * 1.2) + col_idx * 0.12) + 1) / 2
                                seed = (row_idx * 1315423911) ^ (col_idx * 2654435761)
                                phase = (seed % 1000) / 1000.0
                                white_osc = (math.sin(anim_frame_time * 1.5 + phase * 6.28318) + 1) / 2
                                white_factor = (white_osc ** 3) * 0.9
                                sparsity = ((seed >> 3) & 31) / 31.0
                                white_factor = white_factor * (sparsity * 0.8)
                                color = animationtest.final_cell_color(base, norm, row_idx, animationtest.ROWS,
                                                                       time_mod=col_mod, white_factor=white_factor)
                                surf = anim_font.render(ch, True, color)
                                x = animationtest.PADDING + col_idx * anim_char_w
                                anim_surface.blit(surf, (x, y))
                    # scale and blit (also cache the scaled frame so we can show it when paused)
                    try:
                        cur_w, cur_h = screen.get_size()
                        scaled = pygame.transform.smoothscale(anim_surface, (cur_w, cur_h))
                        screen.blit(scaled, (0,0))
                        last_anim_frame = scaled.copy()
                    except Exception:
                        screen.blit(anim_surface, (0,0))
                        try:
                            last_anim_frame = anim_surface.copy()
                        except Exception:
                            last_anim_frame = None
                else:
                    # if we have a cached last frame, show it (freeze); otherwise fallback to BG
                    if last_anim_frame is not None:
                        try:
                            cur_w, cur_h = screen.get_size()
                            # if cached frame is different size, scale it to current window
                            if (last_anim_frame.get_width(), last_anim_frame.get_height()) != (cur_w, cur_h):
                                screen.blit(pygame.transform.smoothscale(last_anim_frame, (cur_w, cur_h)), (0,0))
                            else:
                                screen.blit(last_anim_frame, (0,0))
                        except Exception:
                            screen.fill(BG_COLOR)
                    else:
                        screen.fill(BG_COLOR)
            else:
                # animation disabled: keep last frame visible (freeze) if present
                if last_anim_frame is not None:
                    try:
                        cur_w, cur_h = screen.get_size()
                        if (last_anim_frame.get_width(), last_anim_frame.get_height()) != (cur_w, cur_h):
                            screen.blit(pygame.transform.smoothscale(last_anim_frame, (cur_w, cur_h)), (0,0))
                        else:
                            screen.blit(last_anim_frame, (0,0))
                    except Exception:
                        screen.fill(BG_COLOR)
                else:
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