import os
import sys
import random
import math
import pygame
from pathlib import Path

# Optional: if you want the script to convert PDF -> PNG automatically,
# uncomment the following block and install pdf2image + poppler.
# from pdf2image import convert_from_path

# CONFIG
# If you exported the PDF to a PNG manually, set IMAGE_PATH to that PNG.
# If you want automatic conversion from the uploaded PDF, set PDF_PATH and leave IMAGE_PATH as None.
IMAGE_PATH = "ui_background.png"   # recommended: exported from your PDF
PDF_PATH = "TV - 1.pdf"            # the uploaded PDF filename (if using automatic conversion)
GENERATED_GRAPH_PATH = "graph.png" # optional: external graph image (when available)

WINDOW_TITLE = "UI Demo"
FPS = 60

# UI layout (adjust as needed)
FRAME_PADDING = 20
# Button definitions will be positioned relative to the window size in runtime
BUTTON_SIZE = (160, 48)
BUTTON_MARGIN = 12

# Graph area (left side) as fraction of width
GRAPH_AREA_RECT = None  # computed when we know window size

# Color & style
GREY_FRAME_COLOR = (200, 200, 200)
BACKGROUND_FILL = (30, 30, 30)
BUTTON_BORDER_COLOR = (180, 180, 180)
BUTTON_TEXT_COLOR = (255, 255, 255)
HOVER_OVERLAY = (255, 255, 255, 40)
PRESSED_OVERLAY = (0, 0, 0, 100)

# -----------------------
# helper functions
# -----------------------

def convert_pdf_to_png(pdf_path, output_png="ui_background.png", poppler_path=None):
    """
    Convert first page of pdf to PNG using pdf2image. Requires pdf2image and poppler.
    Returns output path or raises.
    """
    try:
        from pdf2image import convert_from_path
    except Exception as e:
        raise RuntimeError("pdf2image not installed. pip install pdf2image") from e

    # If poppler binaries are not in PATH, pass poppler_path to convert_from_path
    pages = convert_from_path(pdf_path, dpi=150, poppler_path=poppler_path) if poppler_path else convert_from_path(pdf_path, dpi=150)
    if not pages:
        raise RuntimeError("No pages found in PDF")
    pages[0].save(output_png, "PNG")
    return output_png

def generate_placeholder_graph_surface(size):
    """
    Create a semi-transparent surface simulating a rainfall graph.
    Replace this with loading an image produced by your lxml pipeline later.
    """
    w, h = size
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    surf.fill((0, 0, 0, 0))  # fully transparent background

    # draw axes
    axis_color = (220, 220, 220, 180)
    pygame.draw.line(surf, axis_color, (40, h-30), (w-10, h-30), 2)  # x axis
    pygame.draw.line(surf, axis_color, (40, 10), (40, h-30), 2)      # y axis

    # simulate rainfall values and draw bar chart with gradient
    margin_left = 44
    margin_right = 10
    max_bars = max(6, min(20, w // 40))
    bar_w = (w - margin_left - margin_right) / max_bars * 0.75
    gap = ((w - margin_left - margin_right) - (bar_w * max_bars)) / max_bars

    # generate some random rainfall-like values
    values = [random.uniform(0.1, 1.0) * (0.5 + 0.5*math.sin(i/2.0)) for i in range(max_bars)]
    max_val = max(values) if values else 1.0

    for i, val in enumerate(values):
        x = margin_left + i * (bar_w + gap)
        height_bar = (h - 50) * (val / max_val)
        y = (h - 30) - height_bar
        # gradient color
        top_color = (30, 144, 255, 180)   # dodger blue
        bottom_color = (10, 60, 120, 200)
        # draw rectangle with vertical gradient (simple approximation)
        steps = 6
        for s in range(steps):
            r = top_color[0] + (bottom_color[0]-top_color[0]) * (s/steps)
            g = top_color[1] + (bottom_color[1]-top_color[1]) * (s/steps)
            b = top_color[2] + (bottom_color[2]-top_color[2]) * (s/steps)
            a = top_color[3] + (bottom_color[3]-top_color[3]) * (s/steps)
            seg_h = height_bar / steps
            seg_rect = pygame.Rect(int(x), int(y + s*seg_h), int(bar_w), int(seg_h+1))
            surf.fill((int(r), int(g), int(b), int(a)), seg_rect)

        # bar border (semi-transparent)
        pygame.draw.rect(surf, (255,255,255,80), pygame.Rect(int(x), int(y), int(bar_w), int(height_bar)), 1)

    # overlay a semi-transparent area to ensure translucency when blitted
    overlay = pygame.Surface((w, h), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 90))  # darken background slightly
    surf.blit(overlay, (0,0), special_flags=pygame.BLEND_RGBA_SUB)

    return surf

def load_graph_image(path, size):
    """
    Load an image to use as the graph overlay and scale to size.
    If path doesn't exist, return generated placeholder.
    """
    if path and Path(path).exists():
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.smoothscale(img, size)
        # ensure transparency by setting alpha
        temp = pygame.Surface(size, pygame.SRCALPHA)
        temp.blit(img, (0,0))
        # optionally make it semi-transparent
        temp.set_alpha(200)
        return temp
    else:
        return generate_placeholder_graph_surface(size)

# -----------------------
# Main Pygame App
# -----------------------

def main():
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 22)

    # 1) Ensure background image exists; if not, try to convert PDF automatically (optional)
    bg_path = Path(IMAGE_PATH)
    if not bg_path.exists():
        # If IMAGE_PATH missing but PDF exists, try conversion automatically
        pdf_path = Path(PDF_PATH)
        if pdf_path.exists():
            print(f"Background PNG not found. Converting first page of {PDF_PATH} to {IMAGE_PATH} ...")
            try:
                converted = convert_pdf_to_png(str(pdf_path), output_png=IMAGE_PATH)
                print("Converted PDF to PNG:", converted)
            except Exception as e:
                print("Failed to convert PDF -> PNG:", e)
                print("Continuing with a solid color background.")
                bg_path = None
        else:
            print(f"Background image {IMAGE_PATH} not found and PDF {PDF_PATH} not available.")
            bg_path = None
    else:
        bg_path = bg_path

    # load background or fill fallback
    if bg_path and Path(bg_path).exists():
        bg_img = pygame.image.load(str(bg_path)).convert()
        win_w, win_h = bg_img.get_size()
    else:
        # fallback window size
        win_w, win_h = 1024, 600
        bg_img = None

    screen = pygame.display.set_mode((win_w, win_h))
    pygame.display.set_caption(WINDOW_TITLE)

    # compute UI regions
    frame_rect = pygame.Rect(FRAME_PADDING, FRAME_PADDING, win_w - 2*FRAME_PADDING, win_h - 2*FRAME_PADDING)

    # Graph area on left: take 48% width and full height minus paddings
    graph_w = int(frame_rect.width * 0.48)
    graph_h = int(frame_rect.height * 0.9)
    graph_x = frame_rect.left + 20
    graph_y = frame_rect.top + 20
    graph_rect = pygame.Rect(graph_x, graph_y, graph_w, graph_h)

    # Buttons: three stacked vertically near bottom-right inside the frame
    btn_w, btn_h = BUTTON_SIZE
    btn_x = frame_rect.right - btn_w - 24
    # stack bottom-up
    btn_y3 = frame_rect.bottom - 24 - btn_h
    btn_y2 = btn_y3 - btn_h - BUTTON_MARGIN
    btn_y1 = btn_y2 - btn_h - BUTTON_MARGIN

    buttons = [
        {"name": "Load", "rect": pygame.Rect(btn_x, btn_y1, btn_w, btn_h), "action": "load"},
        {"name": "Refresh", "rect": pygame.Rect(btn_x, btn_y2, btn_w, btn_h), "action": "refresh"},
        {"name": "Quit", "rect": pygame.Rect(btn_x, btn_y3, btn_w, btn_h), "action": "quit"},
    ]

    # load initial placeholder or external graph image
    graph_surf = load_graph_image(GENERATED_GRAPH_PATH, (graph_rect.width, graph_rect.height))
    graph_alpha = 180  # semi-transparent global alpha (0-255)
    graph_surf.set_alpha(graph_alpha)

    pressed_button = None

    running = True
    while running:
        mx, my = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    # 'r' to refresh graph (simulate new data)
                    graph_surf = generate_placeholder_graph_surface((graph_rect.width, graph_rect.height))
                    graph_surf.set_alpha(graph_alpha)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for b in buttons:
                        if b["rect"].collidepoint(event.pos):
                            pressed_button = b["name"]
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and pressed_button:
                    for b in buttons:
                        if b["name"] == pressed_button and b["rect"].collidepoint(event.pos):
                            # execute action
                            action = b["action"]
                            if action == "quit":
                                running = False
                            elif action == "refresh":
                                # refresh placeholder graph (in real use, reload generated graph image)
                                graph_surf = load_graph_image(GENERATED_GRAPH_PATH, (graph_rect.width, graph_rect.height))
                                graph_surf.set_alpha(graph_alpha)
                                print("Graph refreshed")
                            elif action == "load":
                                # in your workflow, you would run lxml parsing and save an image to GENERATED_GRAPH_PATH,
                                # then load it here. For now we regenerate placeholder.
                                graph_surf = generate_placeholder_graph_surface((graph_rect.width, graph_rect.height))
                                graph_surf.set_alpha(graph_alpha)
                                print("Load action (placeholder)")
                            else:
                                print("Button action:", action)
                    pressed_button = None

        # draw
        if bg_img:
            screen.blit(bg_img, (0,0))
        else:
            screen.fill(BACKGROUND_FILL)

        # draw grey frame (semi-3D effect)
        pygame.draw.rect(screen, GREY_FRAME_COLOR, frame_rect, border_radius=6)
        inner = frame_rect.inflate(-6, -6)
        pygame.draw.rect(screen, (240,240,240), inner, 2, border_radius=6)

        # draw graph area background (slightly darker than frame)
        graph_bg = pygame.Surface((graph_rect.width, graph_rect.height))
        graph_bg.fill((245, 245, 245))
        graph_bg.set_alpha(16)
        screen.blit(graph_bg, (graph_rect.left, graph_rect.top))

        # blit semi-transparent graph onto left area
        screen.blit(graph_surf, (graph_rect.left, graph_rect.top))

        # optional: draw border around graph area
        pygame.draw.rect(screen, (180,180,180), graph_rect, 1, border_radius=4)

        # draw buttons
        for b in buttons:
            rect = b["rect"]
            # base fill (transparent so background shows)
            base = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
            base.fill((0,0,0,0))
            screen.blit(base, (rect.x, rect.y))

            is_hover = rect.collidepoint((mx, my))
            is_pressed = (pressed_button == b["name"] and mouse_pressed)
            overlay = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
            if is_pressed:
                overlay.fill(PRESSED_OVERLAY)
            elif is_hover:
                overlay.fill(HOVER_OVERLAY)
            else:
                overlay.fill((0,0,0,0))
            screen.blit(overlay, (rect.x, rect.y))

            # border and label
            pygame.draw.rect(screen, BUTTON_BORDER_COLOR, rect, 1, border_radius=6)
            label_surf = font.render(b["name"], True, BUTTON_TEXT_COLOR)
            label_rect = label_surf.get_rect(center=rect.center)
            screen.blit(label_surf, label_rect)

        # optional status text
        help_text = "Press R to regenerate placeholder graph. Replace graph with your lxml-generated image: " + GENERATED_GRAPH_PATH
        help_s = font.render(help_text, True, (220,220,220))
        screen.blit(help_s, (FRAME_PADDING+10, win_h - FRAME_PADDING - 22))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
