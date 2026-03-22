from datetime import datetime
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


def bold_font(font_size):
    return ImageFont.truetype(HankenGroteskBold, int(font_size * scale_size))

def medium_font(font_size):
    return ImageFont.truetype(HankenGroteskMedium, int(font_size * scale_size))


def create_image():
    img = Image.new("P", resolution)
    img.putpalette(palette)
    draw = ImageDraw.Draw(img)

    for y in range(resolution[1]):
        for x in range(resolution[0]):
            img.putpixel((x, y), WHITE)

    now = datetime.now()
    time_str = now.strftime("%H:%M")
    date_str = now.strftime("%Y.%m.%d")
    weekday_str = now.strftime("%A")

    (w, h) = resolution

    # 時刻を中央に大きく表示
    time_font = bold_font(80)
    _, _, tw, th = time_font.getbbox(time_str)
    draw.text(((w - tw) // 2, (h - th) // 2 - 20), time_str, BLACK, font=time_font)

    # 日付と曜日を時刻の下に表示
    date_font = medium_font(18)
    date_text = f"{date_str}  {weekday_str}"
    _, _, dw, dh = date_font.getbbox(date_text)
    draw.text(((w - dw) // 2, (h - th) // 2 - 20 + th + 12), date_text, BLACK, font=date_font)

    img = ImageOps.expand(img, border=padding, fill=WHITE)
    return img
