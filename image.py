#!/usr/bin/env python3

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
GREEN = 2
BLUE = 3
RED = 4
YELLOW = 5
ORANGE = 6

weather_icon_map = {
    "Clear": "\uf00d",          # ☀ 晴れ
    "Clouds": "\uf013",         # ☁ 曇り
    "Partly Cloudy": "\uf002",  # 🌤 部分的に曇り（Clouds に統合可）
    "Overcast": "\uf013",       # ☁ どんより曇り
    "Fog": "\uf014",            # 🌫 霧
    "Mist": "\uf014",           # 🌫 もや
    "Haze": "\uf0b6",           # 🌫 かすみ
    "Smoke": "\uf062",          # 🌁 煙
    "Dust": "\uf063",           # 🌪 砂埃
    "Sand": "\uf063",           # 🏜 砂嵐
    "Ash": "\uf063",            # 🌋 火山灰
    "Rain": "\uf019",           # 🌧 雨
    "Drizzle": "\uf01a",        # 🌦 小雨
    "Thunderstorm": "\uf01e",   # ⛈ 雷雨
    "Snow": "\uf01b",           # ❄ 雪
    "Sleet": "\uf0b5",          # 🌨 みぞれ
    "Hail": "\uf015",           # 🌨 あられ
    "Tornado": "\uf056",        # 🌪 竜巻
    "Squall": "\uf050",         # 💨 スコール
    "Hurricane": "\uf073",      # 🌀 ハリケーン
    "Windy": "\uf021",          # 🌬 風
    "Hot": "\uf072",            # 🔥 暑い
    "Cold": "\uf076",           # ❄ 寒い
    "Unknown": "\uf07b"         # ❓ 不明
}

def getsize(font, text):
    _, _, right, bottom = font.getbbox(text)
    return (right, bottom)

def put_text_left(draw, x, y, font, text, color):
    text_w, text_h = getsize(font, text)
    draw.text((x, y), text, color, font=font)
    return (text_w, text_h)

def put_text_rigth(draw, x, y, font, text, color):
    (width, _) = resolution
    text_w, text_h = getsize(font, text)
    draw.text((width - text_w - x, y), text, color, font=font)
    return (text_w, text_h)

# Load the fonts
def bold_font(font_size):
    return ImageFont.truetype(HankenGroteskBold, int(font_size * scale_size))

def medium_font(font_size):
    return ImageFont.truetype(HankenGroteskMedium, int(font_size * scale_size))

def weather_font(font_size):
    return ImageFont.truetype('./weathericons-regular-webfont.ttf', int(font_size * scale_size))

weather_result = weather_api.get_current_weather()
weather_forecast = weather_api.get_forecast_weather(datetime.now().timestamp())

def _draw_wether_info(draw):
    weather_info_y = 80
    weather_code = weather_result['weatherCode']
    weather_description = weather_result['weatherDescription']
    (_, weather_name_h) = put_text_rigth(draw, 0, weather_info_y, medium_font(12), weather_description, BLACK)
    put_text_rigth(draw, 20, weather_info_y + weather_name_h, weather_font(58), weather_icon_map[weather_code], BLACK)

    temp_info_y = 80
    weather_temp = weather_result['temp']
    (_, temperature_text_h) = put_text_left(draw, 0, temp_info_y, medium_font(12), "Temperature", BLACK)
    (temp_text_w, _) = put_text_left(draw, 0, temp_info_y + temperature_text_h, bold_font(42), str(weather_temp), BLACK)
    put_text_left(draw, temp_text_w + 4, temp_info_y + temperature_text_h, weather_font(30), "\uf03c", BLACK)

def _draw_pop_line(draw):
    LEN = 16
    (EPAPER_WIDTH, EPAPER_HEIGHT) = resolution
    GRAPH_HEIGHT = 100

    GRAPH_LEFT_MARGIN = 10
    GRAPH_RIGHT_MARGIN = 10
    GRAPH_TOP_MARGIN = 0
    GRAPH_BOTTOM_MARGIN = 20

    graph_region_top = EPAPER_HEIGHT - GRAPH_HEIGHT
    graph_draw_top = graph_region_top + GRAPH_TOP_MARGIN
    graph_draw_bottom = EPAPER_HEIGHT - GRAPH_BOTTOM_MARGIN
    graph_draw_left = GRAPH_LEFT_MARGIN
    graph_draw_right = EPAPER_WIDTH - GRAPH_RIGHT_MARGIN
    graph_draw_width = graph_draw_right - graph_draw_left
    graph_draw_height = graph_draw_bottom - graph_draw_top

    draw.line([(graph_draw_left, graph_draw_bottom), (graph_draw_right, graph_draw_bottom)],
              fill=BLACK, width=1)
    draw.line([(graph_draw_left, graph_draw_top), (graph_draw_left, graph_draw_bottom)],
              fill=BLACK, width=1)

    hours = weather_forecast['date_list'][:LEN]
    precipitation_probs = weather_forecast['pop_list'][:LEN]
    temperatures = weather_forecast['temperature_list'][:LEN]

    def scale_y_precip(value):
        return graph_draw_bottom - value * graph_draw_height

    min_temp, max_temp = min(temperatures), max(temperatures)
    def scale_y_temp(value):
        return graph_draw_bottom - ((value - min_temp) / (max_temp - min_temp)) * graph_draw_height

    def scale_x(index):
        return graph_draw_left + index * (graph_draw_width) / (LEN - 1)

    precip_points = [(scale_x(i), scale_y_precip(precipitation_probs[i])) for i in range(LEN)]
    draw.line(precip_points, fill=BLUE, width=2)

    temp_points = [(scale_x(i), scale_y_temp(temperatures[i])) for i in range(LEN)]
    draw.line(temp_points, fill=RED, width=2)

    for i, hour in enumerate(hours):
        dt = datetime.fromisoformat(hour)
        if(dt.hour != 0):
            continue
        t = dt.strftime('%m/%d')
        x = scale_x(i)
        draw.text((x, graph_draw_bottom + 2), t, BLACK, font=medium_font(8))
        draw.line([(x, graph_draw_top), (x, graph_draw_bottom)], fill=BLACK, width=1)

    font = medium_font(6)
    legend_x = graph_draw_left + 5
    legend_y = graph_draw_top - 20
    legend_size = 10  # 四角形のサイズ

    draw.rectangle([(legend_x, legend_y), (legend_x + legend_size, legend_y + legend_size)], fill=BLUE)
    draw.text((legend_x + legend_size + 5, legend_y - 3), "pop", fill=BLACK, font=font)

    legend_x += 50
    draw.rectangle([(legend_x, legend_y), (legend_x + legend_size, legend_y + legend_size)], fill=RED)
    draw.text((legend_x + legend_size + 5, legend_y - 3), "temperature", fill=BLACK, font=font)


def create_image():
    img = Image.new("P", resolution)
    img.putpalette(palette)
    draw = ImageDraw.Draw(img)

    for y in range(0, resolution[1]):
        for x in range(0, resolution[0]):
            img.putpixel((x, y), WHITE)

    now = datetime.now()
    date_str = now.strftime("%B %d")
    weekday_str = now.strftime("%a")
    put_text_left(draw, 0, 0, bold_font(30), date_str, BLACK)
    put_text_rigth(draw, 0, 0, bold_font(26), weekday_str, BLACK)

    _draw_wether_info(draw)
    _draw_pop_line(draw)

    img = ImageOps.expand(img, border=padding, fill=WHITE)
    return img

if __name__ == "__main__":
    img = create_image()
    img.show()

