import math
import time
import pygame as pygame
import sys

# --- 配置 ---
RAIN_DATA = [15.2, 8.7, 45.3, 78.9, 156.4, 234.7, 298.5, 267.3, 189.6, 67.8, 23.4, 12.1]

# 畫面格數（可調）
COLS = 100   # 字元列寬（降低寬度以符合視窗）
ROWS = 36    # 字元列高

# 視窗與字型大小（可調）
FONT_SIZE = 14
PADDING = 8
FPS = 30

# ASCII 字元從「密」到「稀」
ASCII_CHARS = "@%#*+=-:. "  # 最後一個是空白

# 顏色（可調）
BG_COLOR = (6, 10, 30)
TEXT_COLOR = (210, 230, 255)
ACCENT_COLOR = (80, 200, 220)

# --- 生成函式（與之前邏輯一致，僅字元改為 ASCII） ---
def generate_fluid_pattern(data, time_frame, cols=COLS, rows=ROWS):
    max_val = max(data) if data else 1.0
    grid = []
    for y in range(rows):
        row_chars = []
        for x in range(cols):
            data_index = int((x / cols) * len(data))
            intensity = data[data_index] / max_val

            flowX = x + (time_frame * 0.2)
            flowY = y - (time_frame * 0.8)
            wave1 = math.sin((x * 0.18) + (flowY * 0.12) + (time_frame * 0.05)) * 0.5 + 0.5
            wave2 = math.sin((x * 0.08) + (flowY * 0.22) + (time_frame * 0.08)) * 0.4 + 0.6
            wave3 = math.cos((x * 0.25) + (flowY * 0.08) - (time_frame * 0.06)) * 0.5 + 0.5
            wave4 = math.sin((flowX * 0.15) + (flowY * 0.35) + (time_frame * 0.1)) * 0.3 + 0.7

            horizontalFlow = math.sin((x * 0.15) + (time_frame * 0.12)) * 0.3
            diagonalFlow = math.cos((x * 0.08) + (y * 0.08) + (time_frame * 0.09)) * 0.25

            combined = (wave1 + wave2 + wave3 + wave4) / 4.0 + horizontalFlow + diagonalFlow
            modulated = combined * intensity

            noise1 = math.sin(x * 0.5 + flowY * 0.4 + time_frame * 0.15) * 0.2
            noise2 = math.cos(x * 0.7 + y * 0.3 + time_frame * 0.12) * 0.15
            randomness = math.sin(x * 1.2 + y * 0.8 + time_frame * 0.18) * math.cos(x * 0.6 + y * 1.1) * 0.25
            final = modulated + noise1 + noise2 + randomness

            charRandom = math.sin(x * 0.3 + y * 0.5 + time_frame * 0.1) * 0.1
            adjustedFinal = final + charRandom

            # 把 adjustedFinal 正規化到 0..1，再選 ASCII 字元
            # 先把值壓縮到 -1..1 再轉成 0..1
            norm = (math.tanh(adjustedFinal) + 1.0) / 2.0  # 平滑映射
            idx = int(norm * (len(ASCII_CHARS) - 1))
            ch = ASCII_CHARS[max(0, min(len(ASCII_CHARS) - 1, idx))]
            row_chars.append(ch)
        grid.append(''.join(row_chars))
    return grid

# --- Pygame 初始化與主迴圈 ---
def main():
    pygame.init()

    # 優先嘗試 monospace 字型
    monos = pygame.font.match_font('consolas, courier, monospace')  # 嘗試找到 monospace
    if monos:
        font = pygame.font.Font(monos, FONT_SIZE)
    else:
        font = pygame.font.SysFont('couriernew', FONT_SIZE)

    # 測量字元大小
    sample_surf = font.render('M', True, (255,255,255))
    char_w, char_h = sample_surf.get_size()

    window_width = char_w * COLS + PADDING * 2
    window_height = char_h * ROWS + PADDING * 2

    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('Rain Art - ASCII (Pygame)')

    clock = pygame.time.Clock()
    frame = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pattern = generate_fluid_pattern(RAIN_DATA, frame, cols=COLS, rows=ROWS)

        # 背景填色
        screen.fill(BG_COLOR)

        # 繪製字元到畫面（整行渲染）
        for row_idx, line in enumerate(pattern):
            y = PADDING + row_idx * char_h
            trow = row_idx / max(1, ROWS - 1)
            color = (
                int(TEXT_COLOR[0] * (1-trow) + ACCENT_COLOR[0] * trow),
                int(TEXT_COLOR[1] * (1-trow) + ACCENT_COLOR[1] * trow),
                int(TEXT_COLOR[2] * (1-trow) + ACCENT_COLOR[2] * trow),
            )
            surf = font.render(line, True, color)
            screen.blit(surf, (PADDING, y))

        pygame.display.flip()
        frame += 1
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
