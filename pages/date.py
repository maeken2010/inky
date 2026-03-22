from datetime import datetime
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from PIL import Image, ImageDraw, ImageFont, ImageOps

import weather_api

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
YELLOW = 5


def bold_font(font_size):
    return ImageFont.truetype(HankenGroteskBold, int(font_size * scale_size))

def medium_font(font_size):
    return ImageFont.truetype(HankenGroteskMedium, int(font_size * scale_size))


def _get_moon_phase(date):
    """月相を0〜1で返す（0=新月, 0.5=満月）"""
    known_new_moon = datetime(2000, 1, 6, 18, 14)
    cycle = 29.53059
    days_since = (date - known_new_moon).total_seconds() / 86400
    return (days_since % cycle) / cycle


def _moon_phase_name(phase):
    if phase < 0.0625:  return "New Moon"
    if phase < 0.1875:  return "Waxing Crescent"
    if phase < 0.3125:  return "First Quarter"
    if phase < 0.4375:  return "Waxing Gibbous"
    if phase < 0.5625:  return "Full Moon"
    if phase < 0.6875:  return "Waning Gibbous"
    if phase < 0.8125:  return "Last Quarter"
    return "Waning Crescent"


def _draw_moon(draw, cx, cy, r, phase):
    """月の満ち欠けを描画する"""
    bbox = [(cx - r, cy - r), (cx + r, cy + r)]

    if phase < 0.5:
        # 上弦（右側が光っている）
        draw.ellipse(bbox, fill=BLACK)
        draw.chord(bbox, -90, 90, fill=WHITE)
        ew = int(r * (1 - 4 * phase))
        if ew > 0:
            draw.ellipse([(cx - ew, cy - r), (cx + ew, cy + r)], fill=BLACK)
        elif ew < 0:
            draw.ellipse([(cx + ew, cy - r), (cx - ew, cy + r)], fill=WHITE)
    else:
        # 下弦（左側が光っている）
        draw.ellipse(bbox, fill=BLACK)
        draw.chord(bbox, 90, 270, fill=WHITE)
        ew = int(r * (4 * (phase - 0.5) - 1))
        if ew < 0:
            draw.ellipse([(cx + ew, cy - r), (cx - ew, cy + r)], fill=WHITE)
        elif ew > 0:
            draw.ellipse([(cx - ew, cy - r), (cx + ew, cy + r)], fill=BLACK)

    draw.ellipse(bbox, outline=BLACK, width=2)


def create_image():
    weather = weather_api.get_current_weather()

    img = Image.new("P", resolution)
    img.putpalette(palette)
    draw = ImageDraw.Draw(img)

    for y in range(resolution[1]):
        for x in range(resolution[0]):
            img.putpixel((x, y), WHITE)

    now = datetime.now()
    W, H = resolution

    # 日付（大きく中央）
    date_font = bold_font(42)
    date_str = now.strftime("%m-%d")
    _, _, dw, dh = date_font.getbbox(date_str)
    date_y = 16
    draw.text(((W - dw) // 2, date_y), date_str, BLACK, font=date_font)

    # 曜日
    weekday_font = medium_font(18)
    weekday_str = now.strftime("%A")
    _, _, ww, wh = weekday_font.getbbox(weekday_str)
    weekday_y = date_y + dh + 6
    draw.text(((W - ww) // 2, weekday_y), weekday_str, BLACK, font=weekday_font)

    # 区切り線
    divider_y = weekday_y + wh + 14
    draw.line([(0, divider_y), (W, divider_y)], fill=BLACK, width=1)

    # 日の出・日の入り
    sunrise_dt = datetime.fromtimestamp(weather['sunrise'])
    sunset_dt = datetime.fromtimestamp(weather['sunset'])

    label_font = medium_font(11)
    time_font = bold_font(26)

    sun_y = divider_y + 16
    _, _, lw, lh = label_font.getbbox("Sunrise")
    _, _, tw, th = time_font.getbbox("00:00")

    # 左: 日の出
    rise_x = W // 4 - tw // 2
    draw.text((rise_x, sun_y), "Sunrise", BLACK, font=label_font)
    draw.text((rise_x, sun_y + lh + 4), sunrise_dt.strftime("%H:%M"), BLACK, font=time_font)

    # 右: 日の入り
    set_x = W * 3 // 4 - tw // 2
    draw.text((set_x, sun_y), "Sunset", BLACK, font=label_font)
    draw.text((set_x, sun_y + lh + 4), sunset_dt.strftime("%H:%M"), BLACK, font=time_font)

    # 区切り線
    divider2_y = sun_y + lh + 4 + th + 14
    draw.line([(0, divider2_y), (W, divider2_y)], fill=BLACK, width=1)

    # 月の満ち欠け
    from datetime import timedelta
    phase = _get_moon_phase(now)
    cycle = 29.53059
    days_to_full = ((0.5 - phase) % 1.0) * cycle
    next_full_moon = now + timedelta(days=days_to_full)

    moon_r = 50
    moon_cx = W // 3
    moon_cy = divider2_y + 16 + moon_r
    _draw_moon(draw, moon_cx, moon_cy, moon_r, phase)

    # 次の満月
    phase_x = moon_cx + moon_r + 24
    label_font2 = medium_font(11)
    full_moon_font = bold_font(18)
    _, _, _, llh = label_font2.getbbox("Next Full Moon")
    _, _, _, flh = full_moon_font.getbbox("00-00")
    info_y = moon_cy - (llh + 6 + flh) // 2
    draw.text((phase_x, info_y), "Next Full Moon", BLACK, font=label_font2)
    draw.text((phase_x, info_y + llh + 6), next_full_moon.strftime("%m-%d"), BLACK, font=full_moon_font)

    img = ImageOps.expand(img, border=padding, fill=WHITE)
    return img
