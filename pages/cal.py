import calendar
from datetime import datetime, date
import jpholiday
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from PIL import Image, ImageDraw, ImageFont, ImageOps

palette = [
    0, 0, 0,       # 色 0: 黒
    255, 255, 255, # 色 1: 白
    0, 255, 0,     # 色 2: 緑
    0, 0, 255,     # 色 3: 青
    255, 0, 0,     # 色 4: 赤
    255, 255, 0,   # 色 5: 黄
    255, 165, 0    # 色 6: 橙（オレンジ）
] + [0] * (256 * 3 - 21)

resolution_raw = (600, 448)
padding = 16
resolution = tuple(map(lambda x: x - padding*2, resolution_raw))
scale_size = 2.20
BLACK = 0
WHITE = 1
BLUE = 3
RED = 4
ORANGE = 6

DAY_HEADERS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
DAY_COLORS  = [RED,   BLACK, BLACK, BLACK, BLACK, BLACK, BLUE]


def bold_font(font_size):
    return ImageFont.truetype(HankenGroteskBold, int(font_size * scale_size))

def medium_font(font_size):
    return ImageFont.truetype(HankenGroteskMedium, int(font_size * scale_size))


def create_image():
    now = datetime.now()
    year, month, today = now.year, now.month, now.day

    img = Image.new("P", resolution)
    img.putpalette(palette)
    draw = ImageDraw.Draw(img)

    for y in range(resolution[1]):
        for x in range(resolution[0]):
            img.putpixel((x, y), WHITE)

    W, H = resolution

    # タイトル（月・年）
    title_font = bold_font(22)
    title_str = now.strftime("%B %Y")
    _, _, tw, th = title_font.getbbox(title_str)
    title_y = 8
    draw.text(((W - tw) // 2, title_y), title_str, BLACK, font=title_font)

    # 列幅
    col_w = W // 7

    # 曜日ヘッダー
    header_font = medium_font(10)
    header_y = title_y + th + 8
    _, _, _, hh = header_font.getbbox("Sun")
    for i, (label, color) in enumerate(zip(DAY_HEADERS, DAY_COLORS)):
        _, _, lw, _ = header_font.getbbox(label)
        x = i * col_w + (col_w - lw) // 2
        draw.text((x, header_y), label, color, font=header_font)

    # 区切り線
    divider_y = header_y + hh + 6
    draw.line([(0, divider_y), (W, divider_y)], fill=BLACK, width=1)

    # カレンダーグリッド
    weeks = calendar.Calendar(firstweekday=6).monthdayscalendar(year, month)
    row_h = (H - divider_y - 4) // len(weeks)
    day_font = bold_font(16)

    for row, week in enumerate(weeks):
        for col, day in enumerate(week):
            if day == 0:
                continue

            day_str = str(day)
            _, _, dw, dh = day_font.getbbox(day_str)

            cx = col * col_w + col_w // 2
            cy = divider_y + 4 + row * row_h + row_h // 2

            is_holiday = jpholiday.is_holiday(date(year, month, day))

            if day == today:
                r = max(dw, dh) // 2 + 8
                draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=RED)
                draw.text((cx - dw // 2, cy - dh // 2), day_str, WHITE, font=day_font)
            elif is_holiday:
                draw.text((cx - dw // 2, cy - dh // 2), day_str, ORANGE, font=day_font)
            else:
                draw.text((cx - dw // 2, cy - dh // 2), day_str, DAY_COLORS[col], font=day_font)

    img = ImageOps.expand(img, border=padding, fill=WHITE)
    return img
